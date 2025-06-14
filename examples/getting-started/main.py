import pyscratch as pysc
import player, hearts, enemy
from settings import *

background_image = pysc.helper.load_image('assets/vecteezy/my_background.jpg')
pysc.game.set_backdrops([background_image])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE, debug_draw=False)

