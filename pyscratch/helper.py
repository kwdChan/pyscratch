from pathlib import Path
from typing import Dict, Union
import random

import pygame
import numpy as np


def cap(v, min_v, max_v):
    return max(min(max_v, v), min_v)

def random_number(min_v, max_v):

    return random.random()*(max_v-min_v)+min_v


def load_image(path):
    return pygame.image.load(path).convert_alpha()


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

def save_frame_from_sprite_sheet(sheet, columns, rows, spacing=0, margin=0, inset=0, folder_path='.', suffix='png'):
    folder_path = Path(folder_path)
    if not folder_path.exists():
        folder_path.mkdir()
    for i in range(columns*rows):
        f = get_frame(sheet, columns, rows, i, spacing, margin, inset)
        pygame.image.save(f, folder_path/f"{i}.{suffix}")

def get_frame_sequence(sheet, columns, rows, indices, spacing, margin, inset):
    return [get_frame(sheet, columns, rows, i, spacing, margin, inset) for i in indices]

def get_frame_dict(sheet, columns, rows, indices_dict, spacing=0, margin=0, inset=0):
    frame_dict = {}
    for k, v in indices_dict.items():
        assert isinstance(v, list) or isinstance(v, tuple)

        frame_dict[k] = get_frame_sequence(sheet, columns, rows, v, spacing, margin, inset)

    return frame_dict

def load_frames_from_folder(folder_path: Union[Path, str]):

    def extract_images(path: Path):
        index2image: Dict[int, pygame.Surface] = {}

        for f in path.iterdir():
            if f.is_dir():
                continue

            assert f.stem.isdigit(), "the file names must be integers"
            index2image[int(f.stem)] = pygame.image.load(f).convert_alpha()
        
        return [index2image[i] for i in sorted(index2image.keys())]
        

    path = Path(folder_path)

    folder_seen = False
    file_seen = False

    frame_dict = {}
    for f in path.iterdir():
        if f.is_dir():
            folder_seen = True
            assert not file_seen
            frame_dict[f.stem] = extract_images(f)
        else:
            file_seen = True
            assert not folder_seen

    if not folder_seen:
        frame_dict[path.stem] = extract_images(path)

    return frame_dict



def create_circle(colour, radius):
    surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(surface, colour, (radius, radius), radius)
    return surface


def create_rect(colour, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, surface.get_rect())
    return surface

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
