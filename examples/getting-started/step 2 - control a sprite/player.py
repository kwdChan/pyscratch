import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")

# free to use any function name
def on_game_start():

    player.set_rotation_style_left_right() # analogous to the motion block: 'set rotation style [left-right]'
    while True:
        if pysc.is_key_pressed('w'): # analogous to the sensing block: 'key [w] pressed'
            player.y -= 4  # analogous to the motion block: change y by [-4]

        if pysc.is_key_pressed('s'):
            player.y += 4

        if pysc.is_key_pressed('a'):
            player.direction = 180  # analogous to the motion block: point in direction [180]
            player.x -= 4
            
        if pysc.is_key_pressed('d'):
            player.direction = 0
            player.x += 4


        # this is analogous to the control block: wait [1/60] seconds
        # because the frame rate is 60, this is basically to wait for one frame
        yield 1/60 

        # unlike scratch, the wait here is necessary. 
        # Without waiting here, python will put everything aside 
        # to attempt to run the loop as quickly as possible and thus 
        # halt everything else in the program.

        
# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)

# or shorter: 
# player.when_game_start().add_handler(on_game_start)

