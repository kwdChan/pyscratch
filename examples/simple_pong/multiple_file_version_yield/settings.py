import pyscratch as pysc
import pygame

# global settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130
paddle_margin = 30


pysc.game.load_sound('bong', 'assets/sound_effects/Metal Clang-SoundBible.com-19572601.wav')

font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size

top_edge, left_edge, bottom_edge, right_edge = pysc.game.create_edges()
# variables shared across the entire game
pysc.game.shared_data['score_left'] = 0
pysc.game.shared_data['score_right'] = 0
