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

        pysc.game['ss_sprite'] = ss_sprite

        
        ss_sprite.lock_to(ss_view, offset=(0,0)) 
        ss_sprite.set_xy((0,0))


        #ss_sprite.set_draggable(True) #TODO: dragging a locked sprite leads to unexpected behaviour

        pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')
    pass

ss_view.when_receive_message('image_selected').add_handler(on_msg_image_selected)

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
    

    spritesheet = pysc.game.shared_data['image_on_right_display'] 

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
    if not ss_view.is_touching_mouse():
        return
    
    if updown == 'up':
        ss_sprite.scale_by(1.05)
    else:
        ss_sprite.scale_by(1/1.05)

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
    for lx in range(n_line_v):
        xpos = (1+lx)*x_step 
        xpos += x0
        pygame.draw.line(surface, colour, (xpos, y0), (xpos, y1))

    for ly in range(n_line_h):
        ypos = (1+ly)*y_step 
        ypos += y0
        pygame.draw.line(surface, colour, (x0, ypos), (x1, ypos))

    return x_step, y_step



    
def draw_selection_rect():
    ss_select_corner2 = pysc.game['ss_select_corner2']
    ss_select_corner1 = pysc.game['ss_select_corner1']
    while True: 
        yield 1/30
        
        ss_view._drawing_manager.frames[0].fill((255,255,255))
        if not pysc.game['x1']:
            continue

        n_col = 1 if not pysc.game['n_col'] else pysc.game['n_col']
        n_row = 1 if not pysc.game['n_row'] else pysc.game['n_row']

        x0, y0 = pysc.game['x0'], pysc.game['y0']
        #x1, y1 = x0+(pysc.game['pixel_x']*n_col),y0+(pysc.game['pixel_y']*n_row)

        x1 = pysc.game['x0']+((pysc.game['x1']-pysc.game['x0'])//n_col)*n_col
        y1 = pysc.game['y0']+((pysc.game['y1']-pysc.game['y0'])//n_row)*n_row
        #y1= pysc.game['y1']


        lt = topleft()
        x0_draw = x0-lt[0]
        x1_draw = x1-lt[0]
        y0_draw = y0-lt[1]
        y1_draw = y1-lt[1]


        x_step, y_step = draw_cutting_rect(
            ss_view._drawing_manager.frames[0],
            (0,0,0),
            x0_draw, y0_draw, x1_draw,  y1_draw,
            pysc.game['n_row'], pysc.game['n_col']
        )
        
        pysc.game['pixel_x'] = x_step
        pysc.game['pixel_y'] = y_step

        #pygame.draw.lines(ss_view._drawing_manager.frames[0], (0,0,0), True, [(x0_draw, y0_draw), (x0_draw, y1_draw), (x1_draw, y1_draw), (x1_draw, y0_draw)])
ss_view.when_game_start().add_handler(draw_selection_rect)
