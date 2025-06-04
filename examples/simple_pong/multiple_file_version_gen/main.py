import pyscratch as pysc
from settings import * 

# import them just to run them. Another quickiness of this structure
import ball, left_paddle, right_paddle, score_boards



pysc.game.broadcast_message('restart', None) # the message can pass data to the callback function

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(60)



