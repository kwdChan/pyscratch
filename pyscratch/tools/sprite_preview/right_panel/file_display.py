from pathlib import Path
from typing import Tuple
import pyscratch as pysc

from utils.render_wrapped_file_name import render_wrapped_file_name
from settings import *

width, height = 100, 140
colour = (130, 130, 130)

spacing = 10
n_cols = 5

def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None



def FileDisplay(path: Path, order: int, panel_top_left):
    sprite = pysc.create_rect_sprite(colour, width, height)
    
    # set the position

    panel_x, panel_y = panel_top_left
    sprite.x = spacing+(order%n_cols)*(width+spacing)+panel_x +width/2
    sprite.y = spacing+(order//n_cols)*(height+spacing)+panel_y +height/2

    # set the display

    surface = try_load_image(path)
    if not surface: 
        # TODO: messy af
        if path.is_file():
            sprite.remove()
            return None
        
        text = render_wrapped_file_name(path.name+'/', 8, DEFAULT_FONT24)
        sprite.draw(text, offset=(width/2, height/2) )
        #sprite.write_text(path.name+'/', DEFAULT_FONT24, offset=(width/2, height/2))
        
    else: 
        image_margin = 20
        text_height = 20
        fit = "horizontal" if surface.get_width() >= surface.get_height() else "vertical"
        surface = pysc.scale_to_fit_aspect(surface, (width-image_margin, height-text_height-image_margin ), fit)
        sprite.draw(surface, (width/2, (height-text_height)/2))
        
        text = render_wrapped_file_name(path.name, 8, DEFAULT_FONT24, color= (255, 255, 255), max_lines=2)
        sprite.draw(text,offset=(width/2, height-20), reset=False)



    sprite.sprite_data['is_file'] = path.is_file()


    def on_click():
        if not path.is_file():
            pysc.game.broadcast_message('folder_update', path)
        else:
            pysc.game.broadcast_message('image_selected', path)
            #pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')



    sprite.when_this_sprite_clicked().add_handler(on_click)


    def on_msg_mode_change(mode):
        if mode == 'nav':
            sprite.show()
            #pysc.game.bring_to_front(sprite)
        else:
            sprite.hide()

    sprite.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)




    return sprite
    
