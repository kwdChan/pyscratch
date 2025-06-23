import pyscratch as pysc
import edges, ball, right_paddle, left_paddle

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

pysc.game['SCREEN_HEIGHT'] = SCREEN_HEIGHT
pysc.game['SCREEN_WIDTH'] = SCREEN_WIDTH

pysc.game.load_sound('pong', 'assets/Metal Clang-SoundBible.com-19572601.wav')


pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60)
