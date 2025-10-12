import pyscratch as pysc
import pygame
game = pysc.game

enemy = pysc.create_single_costume_sprite("assets/fish_red_skeleton_outline.png")

# 4. Variable
game['clicked'] = False
game['score'] = 0
font = pygame.font.Font('assets/Kenney Future.ttf', size=18)
score_display = pysc.create_shared_data_display_sprite('score', font)
#score_display = pysc.create_shared_data_display_sprite('score')

# 3. Flow
# 4. Variable
def movement():
    """
    when_game_start: 
    the movement of the enemy
    """
    score_cool_down = 0
    while True:
        yield 1/game.framerate

        ## 4. Variable
        if (score_cool_down>0):
            score_cool_down -= 1/game.framerate

        if game['clicked']:
            continue 
    
        speed = max(1, (game['score']))
        centre = (game.screen_width/2, game.screen_height/2)

        ## 3. Flow Control
        mouse_x, mouse_y = pysc.get_mouse_pos()
        if enemy.distance_to((mouse_x, mouse_y)) < 200:
            enemy.point_towards_mouse()
            enemy.direction += 180
            enemy.move_indir(speed)
        
        else:
            enemy.point_towards(centre)
            enemy.move_indir(speed)

        ## 4. Variable
        if enemy.distance_to(centre) < 50 and (score_cool_down<=0):
            score_cool_down = .05
            game['score'] -= 1

enemy.when_game_start().add_handler(movement)
        

# 2. Basic Event
# 3. Flow
# 4. Variable
# 5. Sound 
def clicked():
    """
    when the enemy is clicked: 
    spin and reappear
    """

    ##
    game['score'] += 10
    game['clicked'] = True

    ##
    game.play_sound("hit")
    
    ## 3. Flow control (can be simplified to 2. Basic Event)
    t = 1
    for i in range(10):
        enemy.scale_by(0.9)
        enemy.direction += 30
        t -= 0.1
        enemy.set_transparency(t)
        yield 1/game.framerate


    enemy.set_scale(1)
    game['clicked'] = False

    # 2. Basic Event 
    new_x = pysc.random_number(0, game.screen_width)
    new_y = pysc.random_number(0, game.screen_height)

    enemy.x = new_x
    enemy.y = new_y
    enemy.set_transparency(1)
    
 
enemy.when_this_sprite_clicked().add_handler(clicked)


# 6. Backdrop
def game_end(): 
    """
    when_backdrop_switched: 
    hide the sprite 
    """
    enemy.hide()
    score_display.hide()

enemy.when_backdrop_switched(1).add_handler(game_end)

