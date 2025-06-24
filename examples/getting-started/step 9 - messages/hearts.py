import pyscratch as pysc

# create the sprites
heart1 = pysc.create_animated_sprite("assets/hearts")
heart2 = pysc.create_animated_sprite("assets/hearts")
heart3 = pysc.create_animated_sprite("assets/hearts")

# variable definitons should be done outside the event to guarantee the variables is defined before any event try to access it 
pysc.game['health'] = 3

def heart_display():

    heart1.set_xy((100, 100))
    heart1.set_scale(3)

    heart2.set_xy((155, 100))
    heart2.set_scale(3)

    heart3.set_xy((210, 100))
    heart3.set_scale(3)


    while True: 
        if pysc.game['health'] < 3:
            heart3.set_frame(1)

        if pysc.game['health'] < 2:
            heart2.set_frame(1)

        if pysc.game['health'] < 1:
            heart1.set_frame(1)
        
        yield 1/pysc.game['framerate']
    
# ideally, you should do
# `pysc.game.when_game_start([heart1, heart2, heart3])`, so when any of the hearts is removed, the event is removed as well. 
# but we aren't going to remove any of the hearts, so there's no need to do so there. 

pysc.game.when_game_start().add_handler(heart_display)
