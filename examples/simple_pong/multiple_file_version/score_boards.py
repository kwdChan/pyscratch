import pymunk
import pyscratch as pysc
import pygame
from settings import *

# there are three ways to call interact with other objects 
# 1. using import 
#   - simple but messy because it creates a chain dependency between these files
#   - too many imports discourages the opening of new files 

# 2. put into pysc.game.shared_data (add shared dictionary that allows you to put anything in it)
#   - good for just referencing the sprite
#   - very weird if we put a function in it
#   - need to be careful *when* the sprite get added to the shared_data 

# 3. use the message event 
#   - that is to add spawn_ball as a callback to a message event 
#   - and then boardcast the message here

# using import here 
from ball import spawn_ball

# Score display
score_left = pysc.rect_sprite((170, 170, 170), width=100, height=50, pos=(100, SCREEN_HEIGHT//2))
pysc.game.add_sprite(score_left)

score_right = pysc.rect_sprite((170, 170, 170), width=100, height=50, pos=(SCREEN_WIDTH-100, SCREEN_HEIGHT//2))
pysc.game.add_sprite(score_right)

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
    player_ready_event = pysc.game.create_conditional_trigger(
        lambda: pysc.sensing.is_key_pressed('space'),
        repeats=1
    ) 

    def on_player_ready(n): # the n parameter is how many repeats left in the trigger
        spawn_ball()
        pysc.game.hide_sprite(score_left)
        pysc.game.hide_sprite(score_right)


    player_ready_event.add_callback(on_player_ready)



pysc.game.create_messager_trigger('restart').add_callback(show_score)
