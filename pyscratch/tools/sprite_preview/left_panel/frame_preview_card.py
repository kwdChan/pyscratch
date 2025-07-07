"""
broadcast messages: 
    order_change ((old, new))
    preview_click(dict(surface=surface, order=order))
    change_animation_done (frames: List)

    
receice messages:
    change_animation
        reload the animation from the animation path
        remove and create the frame cards for this animation

shared_data:
    scrolling_offset (read only)
    animation_path 
    frame_card_list 
"""

from typing import Dict, List

import numpy as np
import pyscratch as pysc
from pyscratch.sprite import Sprite
from settings import *
from pygame import Surface
from math import floor
from pathlib import Path


# Sprite Function: the frame preview card
FRAME_PREVIEW_MARGIN = 10
preview_width = LEFT_PANEL_WIDTH-FRAME_PREVIEW_MARGIN*2
preview_height = preview_width 

def FramePreviewCard(surface:Surface, order):

    preview_bg = pysc.create_rect_sprite(
        (255, 255, 255),
        preview_width, 
        preview_height
    )
    preview_bg['surface'] = surface
    preview_bg['order'] = order
    preview_bg.oob_limit = np.inf
    
    preview_bg.set_draggable(True)
    

    # set xy
    ypos = FRAME_PREVIEW_MARGIN + order*(preview_height+FRAME_PREVIEW_MARGIN) + preview_height/2
    
    xpos = LEFT_PANEL_WIDTH/2
    preview_bg.set_xy((xpos, ypos))
    preview_bg.y += pysc.game['scrolling_offset']

    # display preview
    image_margin = 20
    fit = "horizontal" if surface.get_width() >= surface.get_height() else "vertical"
    pv_surface = pysc.scale_to_fit_aspect(surface, (preview_width-image_margin, preview_height-image_margin ), fit)
    preview_bg.draw(pv_surface, (preview_width/2, preview_height/2))
    

    # send message on click
    def on_click():


        pysc.game.broadcast_message('preview_click', dict(surface=surface, order=order))
        pysc.game.broadcast_message('show_bin', None)


    preview_bg.when_this_sprite_clicked().add_handler(on_click)


    # scrolling
    def on_scrolling(offset):
        preview_bg.y = ypos + offset
    preview_bg.when_receive_message('scrolling').add_handler(on_scrolling)


        

    # dragging
    def on_mouse_release():
        pysc.game.broadcast_message('hide_bin', None)
        
        left_panel: pysc.Sprite = pysc.game['left_panel']  

        frame_card_list = pysc.game['frame_card_list']



        new_order = ((preview_bg.y-pysc.game['scrolling_offset'])-preview_height/2-FRAME_PREVIEW_MARGIN)/(preview_height+FRAME_PREVIEW_MARGIN)        
        new_order = floor(new_order+0.5)


        preview_bg.x = xpos

        preview_bg.y = ypos + pysc.game['scrolling_offset']

        new_order = min(max(new_order, 0), len(frame_card_list)-1) 

        if not (to_remove := pysc.game['frame_bin'].is_touching_mouse()):
            if not left_panel.is_touching(preview_bg): return
            if new_order == order: return 
            

        print(f"{order} -> {new_order}")

        first_half = frame_card_list[:order]
        second_half = frame_card_list[order+1:] if (order+1)<len(frame_card_list) else []

        temp = first_half + second_half

        #print([c['order'] for c in temp] )

        if not to_remove: 
            temp = temp[:new_order] + [preview_bg] + (temp[new_order:] if (new_order)<len(temp) else [])

        #print([c['order'] for c in temp] )

        write_new_frame_list([f['surface'] for f in temp])

        # update 
        pysc.game.broadcast_message('change_animation', pysc.game['animation_path'])
            
    pysc.game.when_this_sprite_click_released(preview_bg).add_handler(on_mouse_release)

    return preview_bg


def on_cut_sprite_frame_drop(data):
    if not 'animation_path' in pysc.game.shared_data:
        pysc.game.broadcast_message('warning', "Animation not selected yet.")
        return



    sprite: pysc.Sprite = data['sprite']
    surface: Surface = data['surface']
    mos_x, mos_y = data['position']
    frame_card_list = pysc.game['frame_card_list']


    left_panel: pysc.Sprite = pysc.game['left_panel']  
    
    if not left_panel.is_touching_mouse(): return

    

    order = ((mos_y-pysc.game['scrolling_offset'])-preview_height/2-FRAME_PREVIEW_MARGIN)/(preview_height+FRAME_PREVIEW_MARGIN)        
    order = floor(order+0.5)



    frame_card_list = pysc.game['frame_card_list']

    first_half = frame_card_list[:order]
    second_half = frame_card_list[order:] if (order)<len(frame_card_list) else []

    frame_list = [f['surface'] for f in first_half] +[surface]+ [f['surface'] for f in second_half]

    write_new_frame_list(frame_list)

    # update 
    pysc.game.broadcast_message('change_animation', pysc.game['animation_path'])

    sprite.x = sprite['x']
    sprite.y = sprite['y']


pysc.game.when_receive_message('cut_sprite_frame_drop').add_handler(on_cut_sprite_frame_drop)




# helper function
import shutil
def write_new_frame_list(frame_list: List[Surface]):
    # TODO: frame quality degrade over time?
    temp_folder = Path('temp')
    temp_folder.mkdir(exist_ok=True)
    shutil.rmtree(temp_folder)
    temp_folder.mkdir()

    suffix = 'png' # TODO: allow changing suffix 
    for i, f in enumerate(frame_list):
        pygame.image.save(f, temp_folder/f"{i}.{suffix}")

    shutil.rmtree(pysc.game['animation_path'])
    shutil.copytree(temp_folder, pysc.game['animation_path'])
    shutil.rmtree(temp_folder)
    


# event: when there is a change to the animation
# reload the animation from the animation path
pysc.game['frame_card_list'] = []
def on_change_animation(path: Path):

    #pysc.game['scrolling_offset'] = 0



    pysc.game['animation_path'] = path
    for c in pysc.game['frame_card_list']:
        c.remove()
    pysc.game['frame_card_list'] = []

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
            FramePreviewCard(f, i)
        )
        
    pysc.game.broadcast_message("change_animation_done", frames)
            
    
pysc.game.when_receive_message('change_animation').add_handler(on_change_animation)