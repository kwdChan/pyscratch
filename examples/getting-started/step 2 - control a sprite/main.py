import pyscratch as pysc
import player

# start the game
screen_height = 720
screen_width = 1280
framerate = 60

pysc.game.update_screen_mode((screen_width, screen_height))
pysc.game.start(framerate)

