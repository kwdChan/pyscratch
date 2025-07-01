from utils.input_box import IntegerInputBox, FloatInputBoxVerticallyLabel
import pyscratch as pysc
from settings import *

button = pysc.create_rect_sprite((150, 150, 150), 220, 50)
button.write_text('Set current folder as sprite', DEFAULT_FONT24, offset=(110, 25))

def set_xy():
    container = pysc.game['main_bottom_panel']
    button.lock_to(container, (0,0))
    button.x = 0
    button.y = 0
    
button.when_game_start().add_handler(set_xy)


def on_click():
    pysc.game.broadcast_message('change_sprite_selection', pysc.game['path'])
    pass


button.when_this_sprite_clicked().add_handler(on_click)