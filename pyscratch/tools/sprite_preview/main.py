from pathlib import Path
import pyscratch as pysc
from pyscratch.tools.sprite_preview.right_panel import input_box
from settings import *
import left_panel
from right_panel import file_display_area, cut_or_back_button, cut_or_nav_switch, spritesheet_view, cut_parameters


bg = pysc.create_rect((221, 221, 221), SCREEN_WIDTH, SCREEN_HEIGHT)
pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.set_backdrops([bg])
pysc.game.switch_backdrop(0)

pysc.game.broadcast_message('folder_update', Path('assets'))
pysc.game.broadcast_message('cut_or_nav_mode_change', 'nav')


pysc.game.start(30)