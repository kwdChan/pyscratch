import pyscratch as pysc
from settings import * 

import right_paddle, left_paddle, ball, score_display

pysc.game.shared_data['running']=False

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60, debug_draw=False)
