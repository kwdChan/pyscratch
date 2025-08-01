from pathlib import Path
from typing import List, Tuple
import pyscratch as pysc
from pyscratch.sprite import Sprite
from settings import *
from .file_display import FileDisplay
w, h = 50*1.62, 50
colour = (127, 127, 127)
button = pysc.create_rect_sprite(colour, w, h)
button.set_xy((1100, 550))
pysc.game.change_layer(button, 1)

def on_click():
    if pysc.game.shared_data['cut_or_nav_mode'] == 'nav':
        #pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')
        pass
    else:
        pysc.game.broadcast_message('cut', None)
        #pysc.game.broadcast_message('cut_or_nav_mode_change', 'nav')

button.when_this_sprite_clicked().add_handler(on_click)


def on_msg_mode_change(mode):
    pysc.game.shared_data['cut_or_nav_mode'] = mode
    if mode == 'nav':
        button.write_text("...", DEFAULT_FONT24, offset=(w/2, h/2))
    else:
        button.write_text("Cut", DEFAULT_FONT24, offset=(w/2, h/2))


button.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)