"""
shared_data
    animation_dict (order -> animation selection button)
    sprite_folder_path
    path (read): navigation path
    main_bottom_size (read)
    main_bottom_panel (read)

broadcast messages:
    folder_update (navigation path)
    change_sprite_selection (path of the sprite folder)
    change_animation (path of the animation folder)


receive messages:
    change_sprite_selection
        change the animation panel when another sprite is selected
"""


from pathlib import Path
from typing import cast
import pyscratch as pysc
from settings import *

container_width = SCREEN_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH - PANEL_MARGIN*3
container_height = 300

# container
container = pysc.create_rect_sprite((230, 230, 230), container_width, container_height)
container.x = container_width/2+LEFT_PANEL_WIDTH+PANEL_MARGIN
container.y = SCREEN_HEIGHT-container_height/2-PANEL_MARGIN
pysc.game['main_bottom_panel'] = container
pysc.game['main_bottom_size'] = container_width, container_height

# sprite function
def NewButton(text):
    button_w, button_h = 150, 50
    button = pysc.create_rect_sprite((221, 221, 221), button_w, button_h)
    button.write_text(text, DEFAULT_FONT48, colour=(0,0,0), offset=(button_w/2, button_h/2))
    button.lock_to(container, (-(container_width-button_w)/2, -(container_height-button_h)/2), reset_xy=True)
    return button


# sprite: add sprite button
add_sprite_button = NewButton("New Sprite")
add_sprite_button.y=10
add_sprite_button.x=200

# event: the click of the add sprite button
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
    pysc.game.broadcast_message('cut_or_nav_mode_change', 'nav')
    pysc.game.broadcast_message('change_sprite_selection', new_folder)
        
add_sprite_button.when_this_sprite_clicked().add_handler(on_click1)


# sprite function: animation selection
def AnimationSelection(order, path):
    

    w, h = 120, 30
    on_select = pysc.create_rect((150,150, 150), w, h)
    not_on_select = pysc.create_rect((127, 127, 127), w, h)
    sprite = pysc.Sprite(dict(on_select=[on_select], not_on_select=[not_on_select]))

    sprite.lock_to(container, (-(container_width-w)/2, -(container_height-h)/2))
    sprite.x = 3
    sprite.y = order*(h+3)+3

    sprite.set_animation('on_select')
    sprite.write_text(path.stem, DEFAULT_FONT24, offset=(w/2, h/2))

    sprite.set_animation('not_on_select')
    sprite.write_text(path.stem, DEFAULT_FONT24, offset=(w/2, h/2))



    def on_click():
        sprite.set_animation('on_select')

        pysc.game.broadcast_message('change_animation', path)
        pysc.game.broadcast_message('deselect', sprite)


    sprite.when_this_sprite_clicked().add_handler(on_click)


    def on_deselect(s):
        if not sprite is s:
            sprite.set_animation('not_on_select')

    sprite.when_receive_message('deselect').add_handler(on_deselect)

    return sprite

# event: msg: change_sprite_selection: 
# remove and create the animation buttons when sprite change
pysc.game['animation_dict'] = {}
def on_msg_change_sprite_selection(sprite_folder:Path):
    """
    change the animation selection buttons
    """

    pysc.game['sprite_folder_path'] = sprite_folder

    #pysc.game['frame_dict'] = 



    # remove all the old buttons
    for k, v in pysc.game['animation_dict'].items():
        v.remove()
    pysc.game['animation_dict'] = {}

    animation_dict = pysc.game['animation_dict']
    

    # add the new buttons
    c = 0
    for f in sprite_folder.iterdir():
        if f.is_dir():
            animation_dict[c] = AnimationSelection(c, f)
            c+=1

pysc.game.when_receive_message("change_sprite_selection").add_handler(on_msg_change_sprite_selection)




# sprite: add animation button
add_animation_button = NewButton("New Animation")
add_animation_button.x = 370
add_animation_button.y = 10

# event: click of the add animation button  
def on_click2():


    if not (folder_path:= pysc.game.shared_data.get('sprite_folder_path')):
        pysc.game.broadcast_message('warning', "Sprite folder not selected yet")
        return
    
    folder_path = cast(Path, folder_path)
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