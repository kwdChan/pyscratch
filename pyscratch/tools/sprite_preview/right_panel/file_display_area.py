from pathlib import Path
from typing import List, Tuple, cast
import pyscratch as pysc
from pyscratch.sprite import Sprite
from settings import *
from .file_display import FileDisplay

width, height = RIGHT_PANEL_WIDTH, SCREEN_HEIGHT - PANEL_MARGIN - BOTTOM_RIGHT_PANEL_HEIGHT

colour = 255, 255, 255
folder_navigation = pysc.create_rect_sprite(colour, width, height)

folder_navigation.set_xy((SCREEN_WIDTH - PANEL_MARGIN - RIGHT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2-BOTTOM_RIGHT_PANEL_HEIGHT/2))

topleft = folder_navigation.x-width/2, folder_navigation.y-height/2

folder_navigation['file_display_list'] = []

def on_msg_folder_update(path: Path):
    #folder_navigation.sprite_data['path'] = path
    pysc.game.shared_data['path'] = path

    for fdisp in folder_navigation['file_display_list']:
        fdisp.remove()

    folder_navigation['file_display_list']  = []
    file_display_list = folder_navigation['file_display_list'] 

    c = 0
    for f in path.iterdir():
        fdisp = FileDisplay(f, c, topleft)
        if fdisp: 
            c+=1
            file_display_list.append(fdisp)

folder_navigation.when_receive_message('folder_update').add_handler(on_msg_folder_update)


def on_msg_back_nav(_):
    path: Path = pysc.game['path']
    pysc.game.broadcast_message('folder_update', path.parent)


    
folder_navigation.when_receive_message('back_nav').add_handler(on_msg_back_nav)



def on_msg_mode_change(mode):
    if mode == 'nav':
        folder_navigation.show()
        pysc.game.move_to_back(folder_navigation)
    else:
        folder_navigation.hide()

folder_navigation.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)
pysc.game['folder_navigation'] = folder_navigation