from pathlib import Path
from typing import List, Tuple, cast
import pyscratch as pysc
from pyscratch.sprite import Sprite
from settings import *
from .file_display import FileDisplay

width, height = RIGHT_PANEL_WIDTH, SCREEN_HEIGHT - PANEL_MARGIN - BOTTOM_RIGHT_PANEL_HEIGHT

colour = 255, 255, 255, 0
ss_view = pysc.create_rect_sprite(colour, width, height)

ss_view.set_xy((SCREEN_WIDTH - PANEL_MARGIN - RIGHT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2-BOTTOM_RIGHT_PANEL_HEIGHT/2))
ss_view.set_draggable(True)
topleft = ss_view.x-width/2, ss_view.y-height/2
ss_view.private_data['frame_list'] = []

def on_msg_mode_change(mode):
    if not mode == 'nav':
        ss_view.show()
        pysc.game.move_to_back(ss_view)
        for f in ss_view.private_data['frame_list']:
            f.show()

    else:
        ss_view.hide()
        for f in ss_view.private_data['frame_list']:
            f.hide()

ss_view.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)

def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None


def on_msg_image_selected(path):
    #data['path']
    img = try_load_image(path)
    if img: 
        pysc.game.shared_data['image_on_right_display'] = img
        ss_view.draw(img, offset=(width/2, height/2))
    pass

ss_view.when_receive_message('image_selected').add_handler(on_msg_image_selected)

def on_msg_cut(_):
    ss_view.draw(pysc.create_rect((0,0,0,0), 1, 1)) # reset

    if not 'image_on_right_display' in pysc.game.shared_data:
        print('image not selected' )
        return 
    
    for f in ss_view.private_data['frame_list']:
        f.remove()

    ss_view.private_data['frame_list'] = []
    spritesheet = pysc.game.shared_data['image_on_right_display'] 

    n_row =  pysc.game.shared_data['n_row'] 
    n_col =  pysc.game.shared_data['n_col'] 

    if not n_row:
        print('invalid n_row')
        return
    
    if not n_col:
        print('invalid n_col')
        return
    
    for i in range(n_row*n_col):
        print(i)
        frame = pysc.get_frame_from_sprite_sheet(spritesheet, n_col, n_row, i)
        w, h = frame.get_width(), frame.get_height()
        sprite = pysc.Sprite({'always':[frame]})

        spacing = 0
        x = spacing+(i%n_col)*(w + spacing)+topleft[0] +w/2
        y = spacing+(i//n_col)*(h+spacing)+topleft[1] +h/2


        sprite.private_data['x'] = x
        sprite.private_data['y'] = y

        sprite.x = x
        sprite.y = y

        sprite.set_draggable(True)

        ss_view.private_data['frame_list'].append(sprite)







ss_view.when_receive_message('cut').add_handler(on_msg_cut)
