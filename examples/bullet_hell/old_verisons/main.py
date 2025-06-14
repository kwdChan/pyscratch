import random
import re, sys
import numpy as np
import pymunk
from pyscratch import sensing
from pyscratch.sprite import Sprite, create_rect, create_rect_sprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game


import pygame

WIDTH = 720
HEIGHT = 1280


ENEMY_TYPE = 3
PLAYER_TYPE = 2
PLAYER_BULLET_TYPE = 4
EDGE_TYPE = 1

def cap(v, min_v, max_v):



    return max(min(max_v, v), min_v)

game = Game((WIDTH, HEIGHT))
sprite_sheet = pygame.image.load("assets/09493140a07b68502ef63ff423a6da3954d36fd8/Green Effect and Bullet 16x16.png").convert_alpha()

font = pygame.font.SysFont(None, 24)  # None = default font, 48 = font size
game.suppress_type_collision(PLAYER_TYPE, True)


frames = get_frame_dict(sprite_sheet, 36, 13, {
    "spin": [i+4*36 for i in range(14, 17+1)], 
    "star_explosion": [i+4*36 for i in range(19, 22+1)], 
    "heal": [i+1*36 for i in range(24, 28+1)], 
    "circle_explosion": [i+5*36 for i in range(14, 17+1)], 


    "square_bullets": [i+9*36 for i in range(24, 28+1)]+[i+9*36 for i in range(27, 24, -1)], 
    "circle_bullets": [i+8*36 for i in range(24, 28+1)]+[i+8*36 for i in range(27, 24, -1)], 

    "shield": [i+5*36 for i in [17]], 

    "bullet1": [i+3*36 for i in range(7, 7+1)]
})


#game.start(60, 300, False)
