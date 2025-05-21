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