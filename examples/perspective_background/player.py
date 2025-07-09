import pyscratch as pysc
from pyscratch import game


sp = pysc.create_animated_sprite("assets/used_by_examples/perspective_background/the_red_guy_piskel")  

def next_frame():
    while True:
        yield 0.2
        sp.next_frame()
sp.when_game_start().add_handler(next_frame)

def on_game_start():
    sp.x = 1280/2
    sp.y = 720/2
    sp.retrieve_saved_state()
    sp.set_scale(3)
    sp.set_draggable(True)

    sp.set_rotation_style_left_right()
    while True:
    
        yield 1/game.framerate

        is_running = False
        if pysc.is_key_pressed('d'):
            game['centre_x'] += 5
            is_running = True
            sp.direction=0
            
        if pysc.is_key_pressed('a'):
            game['centre_x'] -= 5
            is_running = True
            sp.direction=180

        if pysc.is_key_pressed('w'):
            game['centre_d'] += 5
            is_running = True
            

        if pysc.is_key_pressed('s'):
            game['centre_d'] -= 5
            is_running = True
        
        if is_running:
            sp.set_animation('run')
        else:
            sp.set_animation('idle')

        
            
sp.when_game_start().add_handler(on_game_start)