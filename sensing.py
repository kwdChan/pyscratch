import pygame

def get_key_presses(keys):
    keycodes = [pygame.key.key_code(k) for k in keys]
    result = pygame.key.get_pressed()
    result = [result[c] for c in keycodes]
    return any(result)


def get_mouse_pos():
    return pygame.mouse.get_pos()

def get_mouse_presses(num_buttons=3):
    return pygame.mouse.get_pressed(num_buttons=num_buttons)

def is_touching(game, sprite_a, sprite_b):
    """pymunk"""
    for pair in game.contact_pairs_set:

        if (sprite_a.shape in pair) and (sprite_b.shape in pair):
            return True
    return False


# def is_overlap(sprite_a, sprite_b, rect_or_circle='rect'):
#     """pygame"""
    
#     if rect_or_circle == 'rect':
#         detection_func = pygame.sprite.collide_rect
#     elif rect_or_circle == 'circle':
#         detection_func = pygame.sprite.collide_circle

#     return detection_func(sprite_a, sprite_b)


def is_touching_mouse(sprite):
    return sprite.shape.point_query(pygame.mouse.get_pos()).distance <= 0
    
