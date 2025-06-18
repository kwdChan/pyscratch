from math import ceil, floor
from pathlib import Path
from typing import Dict

from pygame import Surface
import pyscratch as pysc
from settings import *

PANEL_BG_COLOUR = 199, 207, 224
FRAME_PREVIEW_MARGIN = 10

panel = pysc.create_rect_sprite(
    PANEL_BG_COLOUR,
    LEFT_PANEL_WIDTH, 
    SCREEN_HEIGHT# - PANEL_MARGIN*2
)

panel.set_xy((LEFT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2))



def frame_preview_card(surface:Surface, order):
    preview_width = LEFT_PANEL_WIDTH-FRAME_PREVIEW_MARGIN*2
    preview_height = preview_width 
    preview_bg = pysc.create_rect_sprite(
        (255, 255, 255),
        preview_width, 
        preview_height
    )
    preview_bg['surface'] = surface
    preview_bg['order'] = order
    
    preview_bg.set_draggable(True)
    

    # set xy
    ypos = FRAME_PREVIEW_MARGIN + order*(preview_height+FRAME_PREVIEW_MARGIN) + preview_height/2

    
    xpos = LEFT_PANEL_WIDTH/2
    preview_bg.set_xy((xpos, ypos))

    # display preview
    image_margin = 20
    fit = "horizontal" if surface.get_width() >= surface.get_height() else "vertical"
    pv_surface = pysc.scale_to_fit_aspect(surface, (preview_width-image_margin, preview_height-image_margin ), fit)
    preview_bg.draw(pv_surface, (preview_width/2, preview_height/2))
    

    # send message on click
    def on_click():
        pysc.game.broadcast_message('preview_click', dict(surface=surface, order=order))
    preview_bg.when_this_sprite_clicked().add_handler(on_click)


    # scrolling
    def on_scrolling(offset):
        preview_bg.y = ypos + offset
    preview_bg.when_receive_message('scrolling').add_handler(on_scrolling)


    # dragging


    def on_mouse_release(pos, button, updown):
        #print(button)
        if updown == 'down': return
        if not preview_bg.is_touching_mouse(): return 


        new_order = (preview_bg.y-preview_height/2-FRAME_PREVIEW_MARGIN)/(preview_height+FRAME_PREVIEW_MARGIN)
        print(new_order)
        
        new_order = floor(new_order+0.5)
        print(new_order, order)

        preview_bg.y = ypos + pysc.game['scrolling_offset']
        preview_bg.x = xpos         
        if new_order == order: return 


        print(new_order)


        frame_card_list = pysc.game['frame_card_list']

        temp = frame_card_list[:order] + frame_card_list[order+1:]

        temp_order = new_order if new_order<order else new_order-1

        pysc.game.shared_data['frame_card_list'] = temp[:temp_order] + [preview_bg] + temp[temp_order+1:]

        print(pysc.game.shared_data['frame_card_list'] )

        # reorder
        frames = []
        for new_ord, fc in enumerate(pysc.game.shared_data['frame_card_list']):
            pysc.game.broadcast_message("order_change", (fc['order'], new_ord))
            frames.append(fc['surface'])


        # update 
        pysc.game.broadcast_message('change_animation_done', frames)


        def on_order_change(data):
            nonlocal ypos
            print('order_change', data)
            order, new_order = data

            if not order == preview_bg['order']: return 

            ypos = FRAME_PREVIEW_MARGIN + new_order*(preview_height+FRAME_PREVIEW_MARGIN) + preview_height/2
            preview_bg.y = ypos + pysc.game['scrolling_offset']




        preview_bg.when_receive_message('order_change').add_handler(on_order_change)
        


    pysc.game.when_mouse_click([preview_bg]).add_handler(on_mouse_release)
    




    return preview_bg

pysc.game['scrolling_offset'] = 0

def on_mouse_scroll(updown):
    if not panel.is_touching_mouse(): return
    if updown == 'up':
        pysc.game['scrolling_offset'] += 10
    else: 

        pysc.game['scrolling_offset'] -= 10
        
    pysc.game.broadcast_message("scrolling", pysc.game['scrolling_offset'])
    
pysc.game.when_mouse_scroll().add_handler(on_mouse_scroll)

def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None


pysc.game.shared_data['frame_card_list'] = []

def on_change_animation(path: Path):

    pysc.game['scrolling_offset'] = 0
    pysc.game['animation_path'] = path
    for c in pysc.game.shared_data['frame_card_list']:
        c.remove()
    pysc.game.shared_data['frame_card_list'] = []

    def extract_images(path: Path):
        index2image: Dict[int, pygame.Surface] = {}

        for f in path.iterdir():
            if f.is_dir():
                continue

            if not f.stem.isdigit(): 
                print(f'skipping: {f.name}')
                continue
            index2image[int(f.stem)] = pygame.image.load(f).convert_alpha()
        
        return [index2image[i] for i in sorted(index2image.keys())]
        
    try: 
        frames = extract_images(path)
    except:
        print('invalid folder structure.')
        return 
    

    for i, f in enumerate(frames):
        pysc.game.shared_data['frame_card_list'].append(
            frame_preview_card(f, i)
        )
        
    pysc.game.broadcast_message("change_animation_done", frames)
            
    
pysc.game.when_receive_message('change_animation').add_handler(on_change_animation)