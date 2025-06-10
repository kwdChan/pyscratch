import pyscratch as pysc
import player, enemy, hearts
from settings import *

background = pysc.helper.load_image('assets/medium-vecteezy_the-blue-underwater-sea-with_22967094_medium.jpg')
pysc.game.set_backdrops([background])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE, debug_draw=True)

