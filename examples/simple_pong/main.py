import pyscratch as pysc
import pygame
from pyscratch import game

import right_paddle, left_paddle, ball, score_display

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280


game['running']=False
game['score_left'] = 0
game['score_right'] = 0

game.load_sound('pong', 'assets/sound_effects/Metal Clang-SoundBible.com-19572601.wav')

font = pygame.font.SysFont(None, 48)
pysc.create_shared_data_display_sprite('left_score', font, size=(300, 60))

game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game.start(60, use_frame_time=True)
