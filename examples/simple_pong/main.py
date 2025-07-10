import pyscratch as pysc
from settings import * 

import right_paddle, left_paddle, ball, score_display

pysc.game.shared_data['running']=False

pysc.create_shared_data_display_sprite('left_score', font, size=(300, 60))



pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60)
