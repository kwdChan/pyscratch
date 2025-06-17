import pyscratch as pysc
from settings import *

COLOUR = 255, 255, 255
panel = pysc.create_rect_sprite(
    COLOUR,
    RIGHT_PANEL_WIDTH, 
    SCREEN_HEIGHT - PANEL_MARGIN*2
)

panel.set_xy((SCREEN_WIDTH - PANEL_MARGIN - RIGHT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2))

GRAY = 127, 127, 127
sprite_sheet_cutting_buttom = pysc.create_rect_sprite(GRAY, 200, 40)
sprite_sheet_cutting_buttom.write_text('cut sprite sheet', DEFAULT_FONT48, offset=(100, 20))
sprite_sheet_cutting_buttom.lock_to(panel, (0, 0))