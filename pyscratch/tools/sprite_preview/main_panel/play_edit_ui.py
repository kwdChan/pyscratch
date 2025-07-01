from utils.input_box import IntegerInputBox, FloatInputBoxVerticallyLabel
import pyscratch as pysc
from settings import *
frame_itv = FloatInputBoxVerticallyLabel("frame_interval", default_value="0.2")

def set_xy():
    container = pysc.game['main_bottom_panel']
    frame_itv.lock_to(container, (0,0))
    frame_itv.set_xy((200, 30))
    
frame_itv.when_game_start().add_handler(
    set_xy
)

def new_switch(text0, text1, data_key):
    container = pysc.game.shared_data['main_bottom_panel']
    container_width, container_height = pysc.game.shared_data['main_bottom_size']

    button_w, button_h = 80, 50
    button = pysc.create_rect_sprite((221, 221, 221), button_w, button_h)
    
    pysc.game.shared_data[data_key] = False
    button.write_text(text0, DEFAULT_FONT48, colour=(0,0,0), offset=(button_w/2, button_h/2))

    def on_click():
        pysc.game.shared_data[data_key] = not pysc.game.shared_data[data_key]

        if pysc.game.shared_data[data_key]:
            button.write_text(text1, DEFAULT_FONT48, colour=(0,0,0), offset=(button_w/2, button_h/2))
        else:
            button.write_text(text0, DEFAULT_FONT48, colour=(0,0,0), offset=(button_w/2, button_h/2))
    
    button.when_this_sprite_clicked().add_handler(on_click)


    button.lock_to(container, (-(container_width-button_w)/2, -(container_height-button_h)/2), reset_xy=True)
    return button


def create_play_button():
    container = pysc.game.shared_data['main_bottom_panel']

    play_button = new_switch('Play','Pause', 'is_playing')
    play_button.lock_to(container, (0,0))
    
    play_button.set_xy((0, 70))

pysc.game.when_game_start().add_handler(create_play_button)





scale_factor_input = FloatInputBoxVerticallyLabel("scale_factor", "scale_factor_change", default_value="1")

def set_xy2():
    container = pysc.game.shared_data['main_bottom_panel']
    scale_factor_input.lock_to(container, (0,0))
    scale_factor_input.set_xy((200, 120))
    
scale_factor_input.when_game_start().add_handler(
    set_xy2
)

