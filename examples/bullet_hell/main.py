import pyscratch as pysc
import player, player_bullets, enemy

from setting import *

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pysc.create_edge_sprites()
#pysc.game.shared_data['enemy_level'] = 0

pysc.game.start(60, 60, False, event_count=True)