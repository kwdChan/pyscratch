from typing import List
import pygame

def is_key_pressed(keys: List[str]):
    keycodes = [pygame.key.key_code(k) for k in keys]
    result = pygame.key.get_pressed()
    result = [result[c] for c in keycodes]
    return any(result)


def get_mouse_pos():
    return pygame.mouse.get_pos()

def get_mouse_presses():
    return pygame.mouse.get_pressed(num_buttons=3)

def is_touching(game, sprite_a, sprite_b):
    """pymunk"""
    for pair in game.contact_pairs_set:

        if (sprite_a.shape in pair) and (sprite_b.shape in pair):
            return True
    return False

def is_touching_mouse(sprite):
    return sprite.shape.point_query(pygame.mouse.get_pos()).distance <= 0
    
