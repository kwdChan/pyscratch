import pyscratch as pysc
from pyscratch import game
import  trees, player

sur = pysc.create_rect((169,234,126), 1280, 720)
sur_sky = pysc.create_rect((196,241,255), 1280, 200)
sur.blit(sur_sky, (0,0))

game.set_backdrops([sur])
game.switch_backdrop(0)

game.start(show_mouse_position=True, use_frame_time=True)
game.save_sprite_states()

