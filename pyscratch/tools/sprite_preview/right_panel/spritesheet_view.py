"""
pysc.game.broadcast_message
    ("cut_sprite_frame_drop", dict(sprite=sprite, position=pysc.get_mouse_pos()))

"""
from pathlib import Path
from typing import List, Tuple, cast

from pygame import Surface
import pyscratch as pysc
from settings import *

width, height = RIGHT_PANEL_WIDTH, SCREEN_HEIGHT - PANEL_MARGIN - BOTTOM_RIGHT_PANEL_HEIGHT

colour = 255, 255, 255, 0
ss_view = pysc.create_rect_sprite(colour, width, height)

ss_view.set_xy((SCREEN_WIDTH - PANEL_MARGIN - RIGHT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2-BOTTOM_RIGHT_PANEL_HEIGHT/2))
ss_view.set_draggable(True)
topleft = ss_view.x-width/2, ss_view.y-height/2
ss_view['frame_list'] = []



ss_view['spritesheet_sprite'] = None
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
        if ss_sprite := ss_view['spritesheet_sprite']:
            ss_sprite.hide()
            

ss_view.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)

def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None


def on_msg_image_selected(path):
    
    for f in ss_view['frame_list']:
        f.remove()
    ss_view['frame_list'] = []

    img = try_load_image(path)
    if img: 
        pysc.game.shared_data['image_on_right_display'] = img

        if ss_sprite := ss_view['spritesheet_sprite']:
            ss_sprite.remove()

        ss_view['spritesheet_sprite'] = pysc.Sprite({'a':[img]})
        ss_sprite:pysc.Sprite = ss_view['spritesheet_sprite']
        #ss_sprite.lock_to(ss_view, offset=(0,0)) #TODO: dragging a locked sprite leads to unexpected behaviour
        ss_sprite.set_xy((width/2+topleft[0], height/2+topleft[1]))
        ss_sprite.set_draggable(True)

        pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')
    pass

ss_view.when_receive_message('image_selected').add_handler(on_msg_image_selected)

def on_msg_cut(_):
    ss_view.draw(pysc.create_rect((0,0,0,0), 1, 1)) # reset

    if not 'image_on_right_display' in pysc.game.shared_data:
        print('image not selected' )
        return 
    
    for f in ss_view['frame_list']:
        f.remove()
    ss_view['frame_list'] = []

    
    if ss_sprite := ss_view['spritesheet_sprite']:
        ss_sprite.hide()
    

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
        frame = pysc.get_frame_from_sprite_sheet(spritesheet, n_col, n_row, i)
        sprite = SpriteFrameAfterCut(frame, i, ss_sprite.scale_factor, n_col)
        ss_view.private_data['frame_list'].append(sprite)

ss_view.when_receive_message('cut').add_handler(on_msg_cut)



def SpriteFrameAfterCut(surface: Surface, order, scale_factor, n_col):
    w, h = surface.get_width()*scale_factor, surface.get_height()*scale_factor
    sprite = pysc.Sprite({'always':[surface]})
    sprite.scale_by(scale_factor)


    spacing = 0
    x = spacing+(order%n_col)*(w + spacing)+topleft[0] +w/2
    y = spacing+(order//n_col)*(h+spacing)+topleft[1] +h/2
    
    sprite['x'] = x
    sprite['y'] = y

    sprite.set_xy((x,y))
    sprite.set_draggable(True) 



    def on_mouse_release():

        pysc.game.broadcast_message("cut_sprite_frame_drop", dict(surface=surface, sprite=sprite, position=pysc.get_mouse_pos()))
        pass


    
    pysc.game.when_this_sprite_click_released(sprite).add_handler(on_mouse_release)


    return sprite





def on_scroll(updown):
    #if updown.
    ss_sprite:pysc.Sprite = ss_view['spritesheet_sprite']
    if not ss_sprite: return
    if not ss_sprite.is_touching_mouse():
        return
    
    if updown == 'up':
        ss_sprite.scale_by(1.05)
    else:
        ss_sprite.scale_by(1/1.05)

pysc.game.when_mouse_scroll([ss_view]).add_handler(on_scroll)