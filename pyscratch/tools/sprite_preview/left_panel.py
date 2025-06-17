from pathlib import Path

from pygame import Surface
import pyscratch as pysc
from settings import *

PANEL_BG_COLOUR = 199, 207, 224
panel = pysc.create_rect_sprite(
    PANEL_BG_COLOUR,
    LEFT_PANEL_WIDTH, 
    SCREEN_HEIGHT# - PANEL_MARGIN*2
)

panel.set_xy((LEFT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2))

pysc.game.shared_data['preview_list'] = []


def frame_preview(surface:Surface, image_name, order):

    preview_width = LEFT_PANEL_WIDTH-FRAME_PREVIEW_MARGIN*2
     
    preview_height = preview_width + 20
    preview_bg = pysc.create_rect_sprite(
        (255, 255, 255),
        preview_width, 
        preview_height
    )
    ypos = FRAME_PREVIEW_MARGIN + order*(preview_height+FRAME_PREVIEW_MARGIN) + preview_height/2
    xpos = LEFT_PANEL_WIDTH/2

    # set xy
    preview_bg.set_xy((xpos, ypos))

    # write image name
    preview_bg.write_text(image_name, DEFAULT_FONT24, (0, 0, 0), offset=(preview_width/2, preview_height-12))


    # display preview
    # TODO: 
    image_margin = 20
    text_height = 20
    fit = "horizontal" if surface.get_width() >= surface.get_height() else "vertical"
    pv_surface = pysc.scale_to_fit_aspect(surface, (preview_width-image_margin, preview_height-text_height-image_margin ), fit)
    preview_bg.draw(pv_surface, (preview_width/2, (preview_height-text_height)/2), reset=False)
    



    # send message on click
    def on_click():
        pysc.game.broadcast_message('preview_click', dict(surface=surface, order=order, image_name=image_name))

    preview_bg.when_this_sprite_clicked().add_handler(on_click)

    return preview_bg


def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None

def on_receive_folder_change(path: Path):

    for pv in pysc.game.shared_data['preview_list']:
        pv.remove()
    pysc.game.shared_data['preview_list'] = []
    

    count = 0
    for f in path.iterdir():
        if not f.is_file():
            continue

        img = try_load_image(f)
        if not img:
            continue


        pysc.game.shared_data['preview_list'].append(frame_preview(img, f.name, count))
        count += 1

panel.when_receive_message('folder_change').add_handler(on_receive_folder_change)
pysc.game.broadcast_message('folder_change', Path(PATH))




