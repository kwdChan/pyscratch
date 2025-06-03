import pymunk
import pyscratch as pysc
import pygame


# global settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130
paddle_margin = 30


pysc.game.load_sound('bong', 'assets/sound_effects/Metal Clang-SoundBible.com-19572601.wav')

font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size



# 1. create left paddle
left_paddle_sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height, pos=(paddle_margin, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(left_paddle_sprite)
left_paddle_sprite.set_collision_type(1) # enables the collision


## behaviour
## - move by key 'a' and 'd' in a limited space

left_timer_event = pysc.game.when_timer_reset(10) # run every 10ms, repeats=np.inf by default

def check_move_left(n): # the parameter n is the number of repeats left in the trigger. unused in this case.
    movement = 0
    if pysc.sensing.is_key_pressed('w'):
        movement -= 8

    if pysc.sensing.is_key_pressed('s'):
        movement += 8

    left_paddle_sprite.move_xy((0, movement))

    # confine the paddle within the screen
    min_y = paddle_height//2
    max_y = SCREEN_HEIGHT-paddle_height//2
    left_paddle_sprite.y = pysc.helper.cap(left_paddle_sprite.y, min_y, max_y)

left_timer_event.add_callback(check_move_left)


# 2. create right paddle

right_paddle_sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height, pos=(SCREEN_WIDTH-paddle_margin, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(right_paddle_sprite)
right_paddle_sprite.set_collision_type(1)


## behaviour
## - move by key 'up' and 'down' in a limited space
right_timer_event = pysc.game.when_timer_reset(10)

def check_move_right(n):
    movement = 0
    if pysc.sensing.is_key_pressed('up'):
        movement -= 8

    if pysc.sensing.is_key_pressed('down'):
        movement += 8

    right_paddle_sprite.move_xy((0, movement))

    # confine the paddle within the screen
    min_y = paddle_height//2
    max_y = SCREEN_HEIGHT-paddle_height//2
    right_paddle_sprite.y = pysc.helper.cap(right_paddle_sprite.y, min_y, max_y)

right_timer_event.add_callback(check_move_right)



# 3. Create the function that the ball
# the edges are just sprites
top_edge, left_edge, bottom_edge, right_edge = pysc.create_edge_sprites()

# variables shared across the entire game
pysc.game.shared_data['score_left'] = 0
pysc.game.shared_data['score_right'] = 0

def spawn_ball(): 
    """
    to be called when the game restart
    """

    # create the ball
    ball_sprite = pysc.create_circle_sprite(
        (255, 255, 255), 
        radius=25, 
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
        shape_type='circle', # circular collision shape
        body_type=pymunk.Body.DYNAMIC # freely moving body
        )
    #pysc.game.add_sprite(ball_sprite)
    ball_sprite.set_collision_type(1) # allow collision
    ball_sprite.set_elasticity(1.1) # bounce faster and faster

    # random initial velocity
    vx = pysc.helper.random_number(0.7, 1.2) * ((pysc.helper.random_number(0, 1)>0.5)-0.5)
    vy = pysc.helper.random_number(-1, 1)
    ball_sprite.body.velocity = (vx, vy) # a setter method should be added for simplicity

    # behaviour: 
    ## 1. ball hit edge L: score
    ## 2. ball hit edge R: score
    ## 3. ball hit paddle L: sound effect
    ## 4. ball hit paddle R: sound effect
    
    # detect collisions between two specific sprites
    left_edge_event = pysc.game.create_specific_collision_trigger(ball_sprite, left_edge)
    right_edge_event = pysc.game.create_specific_collision_trigger(ball_sprite, right_edge)

    left_paddle_event = pysc.game.create_specific_collision_trigger(ball_sprite, left_paddle_sprite)
    right_paddle_event = pysc.game.create_specific_collision_trigger(ball_sprite, right_paddle_sprite)

    # the "a" parameter is a pymunk object that contains the collision infomation. unused in this case
    def on_hit_left_edge(a):

        pysc.game.shared_data['score_right'] += 1 
        pysc.game.remove_sprite(ball_sprite)
        pysc.game.boardcast_message('restart', None) # boardcast message 

        # optional: resources release 
        left_edge_event.remove()
        right_edge_event.remove()
        left_paddle_event.remove()        
        right_paddle_event.remove()        

    def on_hit_right_edge(a):

        pysc.game.shared_data['score_left'] += 1 
        pysc.game.remove_sprite(ball_sprite)
        pysc.game.boardcast_message('restart', None)

        # optional: resources release 
        left_edge_event.remove()
        right_edge_event.remove()        
        left_paddle_event.remove()        
        right_paddle_event.remove()        
    
    left_paddle_event.add_callback(lambda a: pysc.game.play_sound('bong', 0.5))
    right_paddle_event.add_callback(lambda a: pysc.game.play_sound('bong', 0.5))

    left_edge_event.add_callback(on_hit_left_edge)
    right_edge_event.add_callback(on_hit_right_edge)



# Score display
score_left = pysc.create_rect_sprite((170, 170, 170), width=100, height=50, pos=(100, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(score_left)

score_right = pysc.create_rect_sprite((170, 170, 170), width=100, height=50, pos=(SCREEN_WIDTH-100, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(score_right)

# 
def show_score(data): # this function is called by the message trigger, which pass in some arbitory data. unused in this case 
    """
    show the score

    press space to restart the game
    """
    pysc.game.show_sprite(score_left)
    pysc.game.show_sprite(score_right)

    # if do offset = (0, 0), the top-left corner of the text will 
    # be at the top-left corner of the image of the sprite
    score_left.write_text(str(pysc.game.shared_data['score_left']), font, offset=(40, 10))
    score_right.write_text(str(pysc.game.shared_data['score_right']), font, offset=(40, 10))

    # a conditional trigger takes a function that output a boolean 
    # the condition is checked every iteration of the game loop
    player_ready_event = pysc.game.when_condition_met(
        lambda: pysc.sensing.is_key_pressed('space'),
        repeats=1
    ) 

    def on_player_ready(n): # the n parameter is how many repeats left in the trigger
        spawn_ball()
        pysc.game.hide_sprite(score_left)
        pysc.game.hide_sprite(score_right)


    player_ready_event.add_callback(on_player_ready)


pysc.game.when_receive_message('restart').add_callback(show_score)
pysc.game.boardcast_message('restart', None) # the message can pass data to the callback function

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60)
