"""
msg in:
    show_bin
    hide_bin

shared data
    frame_bin
"""


import pyscratch as pysc
from settings import *


frame_bin = pysc.create_rect_sprite((255, 127, 127), 100, 100)
frame_bin.write_text("bin", DEFAULT_FONT48, offset=(50, 50))

def set_xy():
    
    container = pysc.game['main_bottom_panel']

    frame_bin.hide()
    frame_bin.lock_to(container, (0,0))
    frame_bin.x = 0
    frame_bin.y = 0
    
frame_bin.when_game_start().add_handler(set_xy)


frame_bin.when_receive_message('show_bin').add_handler(lambda d: frame_bin.show())
frame_bin.when_receive_message('hide_bin').add_handler(lambda d: frame_bin.hide())

pysc.game['frame_bin'] = frame_bin