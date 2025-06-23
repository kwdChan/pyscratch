import pyscratch as pysc
import edges, ball

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280


pysc.game['SCREEN_HEIGHT'] = SCREEN_HEIGHT
pysc.game['SCREEN_WIDTH'] = SCREEN_WIDTH


pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60)
