import pyscratch as pysc
from settings import *

# create the sprites
heart1 = pysc.create_animated_sprite("assets/hearts")
heart1.set_xy((100, 100))
heart1.set_scale(3)

heart2 = pysc.create_animated_sprite("assets/hearts")
heart2.set_xy((155, 100))
heart2.set_scale(3)

heart3 = pysc.create_animated_sprite("assets/hearts")
heart3.set_xy((210, 100))
heart3.set_scale(3)


# create variable
pysc.game.shared_data['health'] = 3

# 
def heart_display():
    while True: 
        if pysc.game.shared_data['health'] < 3:
            heart3.set_frame(1)

        if pysc.game.shared_data['health'] < 2:
            heart2.set_frame(1)

        if pysc.game.shared_data['health'] < 1:
            heart1.set_frame(1)
        
        yield 1/FRAMERATE
    
#game_start_event = pysc.game.when_game_start([heart1, heart2, heart3])
game_start_event = pysc.game.when_game_start([heart1, heart2, heart3])
game_start_event.add_callback(heart_display)