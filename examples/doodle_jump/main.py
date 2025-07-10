import pyscratch as pysc
from pyscratch import game
import player, platforms

width = 720
height = 1280

game.update_screen_mode((width, height))
game.start(60, show_mouse_position=True, print_fps=False)