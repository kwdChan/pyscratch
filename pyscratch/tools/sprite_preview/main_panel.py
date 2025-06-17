import pyscratch as pysc
from settings import *

COLOUR = 255, 255, 255
main_panel_width = SCREEN_WIDTH - RIGHT_PANEL_WIDTH - LEFT_PANEL_WIDTH - PANEL_MARGIN*3
main_panel_height = SCREEN_HEIGHT - PANEL_MARGIN*2

panel = pysc.create_rect_sprite(
    COLOUR,
    main_panel_width, 
    main_panel_height
)

panel.set_xy((LEFT_PANEL_WIDTH+PANEL_MARGIN+main_panel_width/2,  SCREEN_HEIGHT/2))


def on_preview_click(data):
    surface = data['surface']
    panel.draw(surface, (main_panel_width/2, main_panel_height/2))


panel.when_receive_message('preview_click').add_handler(on_preview_click)