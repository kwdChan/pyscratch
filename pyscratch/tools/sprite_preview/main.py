from pathlib import Path
import pyscratch as pysc
from pyscratch.tools.sprite_preview import input_box
from pyscratch.tools.sprite_preview.right_panel import back_button, cut_button
from settings import *
from right_panel import file_display_area, spritesheet_view, cut_parameters
from main_panel import sprite_edit_ui, play_edit_ui, animation_display, frame_bin, set_as_sprite_folder
from left_panel import frame_preview_card, frame_preview_panel

bg = pysc.create_rect((221, 221, 221), SCREEN_WIDTH, SCREEN_HEIGHT)
pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.set_backdrops([bg])
pysc.game.switch_backdrop(0)

pysc.game.broadcast_message('folder_update', Path('testing_assets'))
pysc.game.broadcast_message('cut_or_nav_mode_change', 'nav')
#pysc.game.broadcast_message('change_sprite_selection', Path('./testing_assets/cat'))

pysc.game.start(30)