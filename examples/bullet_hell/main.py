import pyscratch as pysc
from pyscratch import game

import player,player_bullet, enemy, enemy_bullet

width = 720
height = 1280
sur = pysc.create_rect((50,50,50), width, height)


game.set_backdrops([sur])
game.switch_backdrop(0)

game.update_screen_mode((width, height))
game.start(show_mouse_position=True, event_count=True)
#=game.save_sprite_states()

