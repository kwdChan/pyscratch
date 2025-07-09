"""
pysc.game.broadcast_message
    ("cut_sprite_frame_drop", dict(sprite=sprite, position=pysc.get_mouse_pos()))

"""
from pathlib import Path
from typing import List, Tuple, cast

import numpy as np
from pygame import Surface
import pyscratch as pysc
from settings import *
game = pysc.game
width, height = RIGHT_PANEL_WIDTH, SCREEN_HEIGHT - PANEL_MARGIN - BOTTOM_RIGHT_PANEL_HEIGHT

colour = 255, 255, 255, 255
ss_view = pysc.create_rect_sprite(colour, width, height)

ss_view.set_xy((SCREEN_WIDTH - PANEL_MARGIN - RIGHT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2-BOTTOM_RIGHT_PANEL_HEIGHT/2))
#ss_view.set_draggable(False)
#topleft = ss_view.x-width/2, ss_view.y-height/2
pysc.game['ss_view'] = ss_view

def topleft():
    return ss_view.x-width/2, ss_view.y-height/2
ss_view['frame_list'] = []

pysc.game['ss_view_topleft'] = topleft()
pysc.game['ss_view_buttom_right'] = ss_view.x+width/2, ss_view.y+height/2



ss_view['spritesheet_sprite'] = None
pysc.game['ss_sprite'] = None
def on_msg_mode_change(mode):
    if not mode == 'nav':
        ss_view.show()
        pysc.game.move_to_back(ss_view)
        for f in ss_view.sprite_data['frame_list']:
            f.show()

    else:
        ss_view.hide()
        for f in ss_view.sprite_data['frame_list']:
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

        pysc.game['ss_sprite'] = ss_sprite
        ss_sprite.oob_limit=np.inf
        ss_sprite['original_width'] = img.get_width()
        ss_sprite['original_height'] = img.get_height()
        game.change_layer(ss_sprite, 0)

        
        #ss_sprite.lock_to(ss_view, offset=(0,0)) 
        #ss_sprite.set_xy((0,0))

        ss_sprite.set_xy((ss_view.rect.centerx, ss_view.rect.centery))
        ss_sprite.set_draggable(True) #TODO: dragging a locked sprite leads to unexpected behaviour

        ss_sprite._drawing_manager.set_mask_threshold(-1)


        pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')
    pass

ss_view.when_receive_message('image_selected').add_handler(on_msg_image_selected)
from itertools import product
def on_msg_cut(_):
    ss_view.draw(pysc.create_rect((0,0,0,0), 1, 1)) # reset

    if not 'image_on_right_display' in pysc.game.shared_data:
        pysc.game.broadcast_message('warning', 'image not selected' )
        return 
    
    for f in ss_view['frame_list']:
        f.remove()
    ss_view['frame_list'] = []

    
    if ss_sprite := ss_view['spritesheet_sprite']:
        ss_sprite.hide()
    

    spritesheet: pygame.Surface = pysc.game.shared_data['image_on_right_display'] 

    n_row =  pysc.game.shared_data['n_row'] 
    n_col =  pysc.game.shared_data['n_col'] 

    if not n_row:
        print('invalid n_row')
        pysc.game.broadcast_message('warning', 'invalid n_row' )
        return
    
    if not n_col:
        print('invalid n_col')
        pysc.game.broadcast_message('warning', 'invalid n_col' )
        return
    n_row = int(n_row)
    n_col = int(n_col)
    print(game['offset_x'], game['offset_y'], game['size_x'], game['size_y'])
    spritesheet_to_cut = spritesheet.subsurface(game['offset_x'], game['offset_y'], game['size_x'], game['size_y'])

    for i, (r, c) in enumerate(product(range(n_row), range(n_col))):
        frame = pysc.get_frame_from_sprite_sheet_by_frame_size(spritesheet_to_cut, game['pixel_x'], game['pixel_y'], c, r)
        sprite = SpriteFrameAfterCut(frame, i, ss_sprite.scale_factor, n_col)
        ss_view['frame_list'].append(sprite)

ss_view.when_receive_message('cut').add_handler(on_msg_cut)



def SpriteFrameAfterCut(surface: Surface, order, scale_factor, n_col):
    w, h = surface.get_width()*scale_factor, surface.get_height()*scale_factor
    sprite = pysc.Sprite({'always':[surface]})
    sprite.oob_limit = np.inf
    sprite.scale_by(scale_factor)


    spacing = 0
    lt = topleft()
    x = spacing+(order%n_col)*(w + spacing)+lt[0] +w/2
    y = spacing+(order//n_col)*(h+spacing)+lt[1] +h/2
    
    sprite['x'] = x
    sprite['y'] = y

    sprite.set_xy((x,y))
    sprite.set_draggable(True) 



    def on_mouse_release():

        pysc.game.broadcast_message("cut_sprite_frame_drop", dict(surface=surface, sprite=sprite, position=pysc.get_mouse_pos()))
        pass


    
    pysc.game.when_this_sprite_click_released(sprite).add_handler(on_mouse_release)


    return sprite



# TODO: The scrolling becomes hard to use because touching only happens in the non-transparent pixels


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
    
    pysc.game.broadcast_message("ss_sprite_scale_change")

pysc.game.when_mouse_scroll([ss_view]).add_handler(on_scroll)



def draw_cutting_rect(surface, colour, x0, y0, x1, y1, n_row, n_col):

    n_row = 1 if not n_row else n_row
    n_col = 1 if not n_col else n_col

    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)

    n_line_h = n_row - 1
    n_line_v = n_col - 1


    pygame.draw.lines(surface, colour, True, [(x0, y0), (x0, y1), (x1, y1), (x1, y0)])

    x_step = (x1 - x0)/n_col # vertical lines
    y_step = (y1 - y0)/n_row # horizontal lines
    # 
    for lx in range(int(n_line_v)):
        xpos = (1+lx)*x_step 
        xpos += x0
        pygame.draw.line(surface, colour, (xpos, y0), (xpos, y1))

    for ly in range(int(n_line_h)):
        ypos = (1+ly)*y_step 
        ypos += y0
        pygame.draw.line(surface, colour, (x0, ypos), (x1, ypos))

    return x_step, y_step



    
def draw_selection_rect():
    cir0, cir1 = pysc.game['c0'], pysc.game['c1']
    while True: 
        yield 1/30
        ss_sprite:pysc.Sprite = ss_view['spritesheet_sprite']
        if not ss_sprite: 
            continue

        if game['pixel_x'] is None: continue
        if game['pixel_y'] is None: continue

        ss_view._drawing_manager.frames[0].fill((255,255,255))

        n_col = 1 if not pysc.game['n_col'] else pysc.game['n_col']
        n_row = 1 if not pysc.game['n_row'] else pysc.game['n_row']


        # top left of the selected rect
        gx0 =  game['offset_x']*ss_sprite.scale_factor + ss_sprite.rect.left  - ss_view.rect.left
        gy0 = game['offset_y']*ss_sprite.scale_factor + ss_sprite.rect.top  - ss_view.rect.top
        
        gx1 = gx0 + game['pixel_x']*n_col*ss_sprite.scale_factor 
        gy1 = gy0 + game['pixel_y']*n_row*ss_sprite.scale_factor


        #pygame.draw.lines(ss_view._drawing_manager.frames[0], (0,0,0), True, [(gx0, gy0), (gx0, gy1), (gx1, gy1), (gx1, gy0)])

        draw_cutting_rect(
            ss_view._drawing_manager.frames[0],
            (0,0,0),
            gx0, gy0, gx1,  gy1,
            pysc.game['n_row'], pysc.game['n_col']
        )       

ss_view.when_game_start().add_handler(draw_selection_rect)
