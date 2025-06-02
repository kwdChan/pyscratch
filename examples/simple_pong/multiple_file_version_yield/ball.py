
import pyscratch as pysc
from settings import *
import pymunk

# the following should not be done in general because the data might not have been defined by this time
## left_paddle_sprite = pysc.game.shared_data['left_paddle_sprite']

def spawn_ball(): 
    """
    to be called when the game restart
    """

    # create the ball
    ball_sprite = pysc.circle_sprite(
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

    left_paddle_event = pysc.game.create_specific_collision_trigger(ball_sprite, pysc.game.shared_data['left_paddle_sprite'])
    right_paddle_event = pysc.game.create_specific_collision_trigger(ball_sprite, pysc.game.shared_data['right_paddle_sprite'])

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
