from pathlib import Path
import time
import pyscratch as pysc
from pyscratch.tools.sprite_preview.input_box import IntegerInputBox
from settings import *

container_width = SCREEN_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH - PANEL_MARGIN*3
container_height = 300

# container
container = pysc.create_rect_sprite((255, 255, 255), container_width, container_height)
container.x = container_width/2+LEFT_PANEL_WIDTH+PANEL_MARGIN
container.y = SCREEN_HEIGHT-container_height/2-PANEL_MARGIN
pysc.game.shared_data['main_bottom_panel'] = container
pysc.game.shared_data['main_bottom_size'] = container_width, container_height
# 
def new_button(text):
    button_w, button_h = 150, 50
    button = pysc.create_rect_sprite((221, 221, 221), button_w, button_h)
    button.write_text(text, DEFAULT_FONT48, colour=(0,0,0), offset=(button_w/2, button_h/2))
    button.lock_to(container, (-(container_width-button_w)/2, -(container_height-button_h)/2), reset_xy=True)
    return button


# add sprite button
add_sprite_button = new_button("new sprite")
add_sprite_button.y=10
add_sprite_button.x=200

def on_click1():
    folder_path: Path = pysc.game.shared_data['path']
    
    c = 0
    while True:
        
        
        new_folder = (folder_path / f"unnamed_sprite_{c}")
        if not new_folder.exists():
            new_folder.mkdir()
            break
        else:
            c+=1

    pysc.game.broadcast_message('folder_update', folder_path)
    pysc.game.broadcast_message('change_sprite_selection', new_folder)
        
add_sprite_button.when_this_sprite_clicked().add_handler(on_click1)


# animation selection
def animation_selection(order, path):
    

    w, h = 120, 30
    colour = 127, 127, 127
    sprite = pysc.create_rect_sprite(colour, w, h)
    sprite.lock_to(container, (-(container_width-w)/2, -(container_height-h)/2))
    sprite.x = 3
    sprite.y = order*(h+3)+3
    sprite.write_text(path.stem, DEFAULT_FONT24, offset=(w/2, h/2))
    sprite.when_this_sprite_clicked().add_handler(lambda: pysc.game.broadcast_message('change_animation', path))
    
    
    
    return sprite

# remove and create the animation buttons when sprite change
pysc.game.shared_data['animation_dict'] = {}
def on_msg_change_sprite_selection(sprite_folder:Path):
    """
    change the animation selection buttons
    """

    pysc.game.shared_data['sprite_folder_path'] = sprite_folder

    # remove all the old buttons
    for k, v in pysc.game.shared_data['animation_dict'].items():
        v.remove()
    pysc.game.shared_data['animation_dict'] = {}

    animation_dict = pysc.game.shared_data['animation_dict']
    

    # add the new buttons
    c = 0
    for f in sprite_folder.iterdir():
        if f.is_dir():
            animation_dict[c] = animation_selection(c, f)
            c+=1

pysc.game.when_receive_message("change_sprite_selection").add_handler(on_msg_change_sprite_selection)




# add animation button
add_animation_button = new_button("new animation")
add_animation_button.x = 400
add_animation_button.y = 10

def on_click2():
    folder_path: Path = pysc.game.shared_data['sprite_folder_path']
    c = 0
    while True:
        
        
        new_folder = (folder_path / f"animation_{c}")
        if not new_folder.exists():
            new_folder.mkdir()
            break
        else:
            c+=1

    pysc.game.broadcast_message('folder_update', pysc.game.shared_data['path'])
    
    # no actual change. just to trigger the update
    pysc.game.broadcast_message('change_sprite_selection', folder_path)

            

add_animation_button.when_this_sprite_clicked().add_handler(on_click2)