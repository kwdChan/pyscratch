import numpy as np
import pyscratch as pysc
from pyscratch import game

game['centre_x'] = 1280/2
game['centre_h'] = 300
game['centre_d'] = 0
def tree_L():
    sp = pysc.create_animated_sprite("assets/used_by_examples/perspective_background/tree_L")  
    sp['d'] = pysc.random_number(100, 2000) 
    sp['world_x'] = pysc.random_number(0, 1000)
    sp.oob_limit=np.inf
    def on_game_start():
        sp.set_frame(int(pysc.random_number(0, 2.99)))
        sp.set_draggable(True)
        d = sp['d']-game['centre_d']
        game.change_layer(sp, 1000-int(sp['d']))
        while True:
            yield 1/game.framerate
            d = sp['d']-game['centre_d']

            new_scale = pysc.cap(300/d, 0.1, 3)
            if new_scale == 3:
                sp.hide()
            else:
                sp.show()
                sp.set_scale(new_scale)
            if d <= 0:
                sp.hide()

            sp.y = -200+game.screen_height-np.arctan(d/game['centre_h'])/np.pi*game.screen_height 
            sp.x = ((sp['world_x']-game['centre_x'])/d + 0.5)*game.screen_width

    sp.when_game_start().add_handler(on_game_start)

    return sp

for i in range(50):
    tree_L()
