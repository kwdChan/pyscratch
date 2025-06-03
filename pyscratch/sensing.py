from typing import List
import pygame
from .game import game

def is_key_pressed(key: str) -> bool:
    keycode = pygame.key.key_code(key)
    result = pygame.key.get_pressed()
    return result[keycode]


def get_mouse_pos():
    return pygame.mouse.get_pos()

def get_mouse_presses():
    return pygame.mouse.get_pressed(num_buttons=3)

def is_touching(sprite_a, sprite_b):
    """pymunk"""
    for pair in game.contact_pairs_set:

        if (sprite_a.shape in pair) and (sprite_b.shape in pair):
            return True
    return False

def is_touching_mouse(sprite):
    return sprite.shape.point_query(pygame.mouse.get_pos()).distance <= 0
    
