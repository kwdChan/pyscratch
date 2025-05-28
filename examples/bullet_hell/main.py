import pyscratch as pysc
import player, player_bullets, enemy

from setting import *

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pysc.game.create_edges()


pysc.game.start(60, 60, False)