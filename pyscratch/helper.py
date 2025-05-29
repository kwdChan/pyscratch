import pygame
import random

def cap(v, min_v, max_v):
    return max(min(max_v, v), min_v)

def random_number(min_v, max_v):

    return random.random()*(max_v-min_v)+min_v


def get_frame(sheet, columns, rows, index, spacing=0, margin=0, inset=0):
    """
    WRITTEN BY CHATGPT
    """
    sheet_rect = sheet.get_rect()

    total_spacing_x = spacing * (columns - 1)
    total_spacing_y = spacing * (rows - 1)

    total_margin_x = margin * 2
    total_margin_y = margin * 2

    frame_width = (sheet_rect.width - total_spacing_x - total_margin_x) // columns
    frame_height = (sheet_rect.height - total_spacing_y - total_margin_y) // rows

    col = index % columns
    row = index // columns

    x = margin + col * (frame_width + spacing)
    y = margin + row * (frame_height + spacing)

    # Apply internal cropping (inset) from all sides
    cropped_rect = pygame.Rect(
        x + inset,
        y + inset,
        frame_width - 2 * inset,
        frame_height - 2 * inset
    )

    return sheet.subsurface(cropped_rect)



def get_frame_sequence(sheet, columns, rows, indices, spacing, margin, inset):
    return [get_frame(sheet, columns, rows, i, spacing, margin, inset) for i in indices]

def get_frame_dict(sheet, columns, rows, indices_dict, spacing=0, margin=0, inset=0):
    frame_dict = {}
    for k, v in indices_dict.items():
        assert isinstance(v, list) or isinstance(v, tuple)

        frame_dict[k] = get_frame_sequence(sheet, columns, rows, v, spacing, margin, inset)

    return frame_dict


import pygame
import numpy as np



def scale_and_tile(image, screen_size, scale_factor):
    """WRITTEN BY AI"""

    img_w, img_h = image.get_size()
    new_img = pygame.transform.smoothscale(image, (int(img_w * scale_factor), int(img_h * scale_factor)))
    new_img_w, new_img_h = new_img.get_size()
    
    tiled_surface = pygame.Surface(screen_size)
    
    for y in range(0, screen_size[1], new_img_h):
        for x in range(0, screen_size[0], new_img_w):
            tiled_surface.blit(new_img, (x, y))
    
    return tiled_surface


def scale_to_fill_screen(image, screen_size):
    """WRITTEN BY AI (lol)"""
    return pygame.transform.smoothscale(image, screen_size)


def scale_to_fit_aspect(image, screen_size, fit='horizontal'):
    """WRITTEN BY AI"""
    img_rect = image.get_rect()
    screen_w, screen_h = screen_size
    img_w, img_h = img_rect.size

    if fit == 'horizontal':
        scale_factor = screen_w / img_w
    elif fit == 'vertical':
        scale_factor = screen_h / img_h
    else:
        raise ValueError("fit must be 'horizontal' or 'vertical'")

    new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
    return pygame.transform.smoothscale(image, new_size)



def set_transparency(image, factor):
    """
    Return a copy of the image with the given factor 
    
    WRITTEN BY AI
    """
    new_image = image.copy()
    new_image.set_alpha(int(factor*255))
    return new_image



def adjust_brightness(image, factor):
    """
    Return a copy of the image with brightness adjusted by the given factor.

    Does not work very well for the transparent background of sprite frames 
    
    WRITTEN BY AI
    """
    new_image = image.copy()
    brightness_surface = pygame.Surface(image.get_size()).convert_alpha()
    brightness_surface.fill((255, 255, 255, 0))  # Start with no change
    
    # Per-pixel operation is slow. Instead, we use special_flags to modulate brightness.
    if factor < 1:
        # Darken using multiply blend mode
        darken_surface = pygame.Surface(image.get_size()).convert_alpha()
        value = int(255 * factor)
        darken_surface.fill((value, value, value))
        new_image.blit(darken_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    elif factor > 1:
        # Brighten by blending in white
        value = int(255 * (factor - 1))
        brighten_surface = pygame.Surface(image.get_size()).convert_alpha()
        brighten_surface.fill((value, value, value))
        new_image.blit(brighten_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    return new_image
