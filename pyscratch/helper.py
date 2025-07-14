"""
Everything in this module is directly under the pyscratch namespace. 
For example, instead of doing `pysc.helper.random_number`,
you can also directly do `pysc.random_number`
"""


from functools import cache
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple, Union
import random

import pygame
import numpy as np


def cap(v:float, min_v:float, max_v:float)->float:
    """
    Cap a value to a range between `min_v` and `max_v`.

    Example
    ```python
    cap(5, 1, 10) # returns 5 
    cap(15, 1, 10) # returns 10
    cap(-10, 1, 10) # returns 1
    
    # a more realistic example usage: keep the sprite within the screen. 
    my_sprite.x = cap(my_sprite.x, 0, SCREEN_WIDTH)
    my_sprite.y = cap(my_sprite.y, 0, SCREEN_HEIGHT)
    ```
    """
    return max(min(max_v, v), min_v)

def random_number(min_v:float, max_v:float) -> float:
    """
    Returns a random number between `min_v` and `max_v`
    """
    return random.random()*(max_v-min_v)+min_v

@cache
def load_image(path: str) -> pygame.Surface:
    """
    Return the `pygame.Surface` given the path to an image. 
    """
    return pygame.image.load(path).convert_alpha()


def get_frame_from_sprite_sheet(
        sheet: pygame.Surface, 
        columns:int, rows:int, index:int, 
        spacing:int=0, margin:int=0, inset:int=0):
    """
    Extract a specific frame from a sprite sheet. 
    
    *You will not need to use this function directly.*

    THIS FUNCTION IS WRITTEN BY AN AI. 


    The index starts from the top-left as 0,
    and increments left-to-right before up-to-down.
    For example, for a 3x3 sheet, the index would be
    ```
    0 1 2
    3 4 5
    6 7 8
    ```
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

def get_frame_from_sprite_sheet_by_frame_size(
        sheet: pygame.Surface, 
        size_x: int, size_y: int,
        c:int, r: int):
    """
    Extract a specific frame from a sprite sheet.
    
    *You will not need to use this function directly.*


    Parameters
    ---
    sheet: pygame.Surface
        The sprite sheet you want to cut
    
    size_x: int
        The x pixel size of the frame
    
    size_y: int
        The y pixel size of the frame

    c: int 
        The column position of the frame

    r: int 
        The row position of the frame
    """
    crop_rect = pygame.Rect(
        c*size_x,
        r*size_y,
        size_x,
        size_y
    )

    return sheet.subsurface(crop_rect)

from PIL import Image, ImageSequence
import pygame

@cache
def load_gif_frames(path) -> List[pygame.Surface]:
    """
    Load a gif file as a list of images (as `pygame.Surface`)

    *You will not need to use this function directly.*

    THIS FUNCTION IS WRITTEN BY AN AI.

    """
    pil = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(pil):
        mode   = frame.convert("RGBA")
        data   = mode.tobytes()
        size   = mode.size
        surf   = pygame.image.frombuffer(data, size, "RGBA").convert_alpha()
        frames.append(surf)
    return frames


@cache
def load_frames_from_gif_folder(folder_path: Path):
    """
    Creates a `frame_dict` that the Sprite constructor takes using 
    the gif files inside a folder. 

    The folder should be organised in the following way: 
    ```
    ├─ player/
        ├─ walking.gif
        ├─ idling.gif
        ├─ jumping.gif
        ...
    ```

    *You will not need to use this function directly.*


    """
    frame_dict = {}
    for f in folder_path.iterdir():
        if f.suffix != '.gif': 
            print(f"ignoring {f.name} (not a gif)")
            continue

        frame_dict[f.stem] = load_gif_frames(f)
    
    return frame_dict




def cut_sprite_sheet(
        sheet: pygame.Surface, 
        columns, rows, 
        spacing=0, margin=0, inset=0, 
        folder_path='.', 
        suffix='png'):
    """
    Split a sprite sheet so each frame is its own image file. 
    
    *You probably won't need to use this function directly.*
    
    Parameters
    ---
    sheet: pygame.Surface
        The sprite sheet image
    columns: int
        The total number of columns of the sheet
    rows: int
        The total number of rows of the sheet
    spacing: int
        Keep it as zero.
    margin: int
        Keep it as zero.
    inset: int
        Keep it as zero.
    folder_path: str
        The path of the destination folder to put the splitted images. 
    suffix: str
        The file extension 
    """
    
    folder_path = Path(folder_path)
    if not folder_path.exists():
        folder_path.mkdir()
    for i in range(columns*rows):
        f = get_frame_from_sprite_sheet(sheet, columns, rows, i, spacing, margin, inset)
        pygame.image.save(f, folder_path/f"{i}.{suffix}")

def _get_frame_sequence(sheet:pygame.Surface, columns:int, rows:int, indices:List[int], spacing:int, margin:int, inset:int):
    """
    **You will not need to use this function directly.**
    """
    return [get_frame_from_sprite_sheet(sheet, columns, rows, i, spacing, margin, inset) for i in indices]

def _get_frame_dict(
        sheet:pygame.Surface, columns:int, rows:int, 
        indices_dict: Dict[str, List[int]], 
        spacing:int=0, margin:int=0, inset:int=0):
    """
    **You will not need to use this function directly.**
    """
    frame_dict = {}
    for k, v in indices_dict.items():
        assert isinstance(v, list) or isinstance(v, tuple)

        frame_dict[k] = _get_frame_sequence(sheet, columns, rows, v, spacing, margin, inset)

    return frame_dict

@cache
def load_frames_from_folder(folder_path: Union[Path, str]):
    """
    Creates a `frame_dict` that the Sprite constructor takes using 
    the images inside a folder. 
    You can use `sprite.create_animated_sprite` instead for convenience.

    The folder should be organised in one of these two ways: 

    **Option 1**: Only one frame mode. *Note that the images must be numbered.*
    ```
    ├─ player/
        ├─ 0.png
        ├─ 1.png
        ├─ 2.png
        ...
    ```

    **Option 2**: Multiple frame modes. *Note that the images must be numbered.*
    ```
    ├─ player/  
        ├─ walking/  
            ├─ 0.png  
            ├─ 1.png  
            ...
        ├─ idling/
            ├─ 0.png
            ├─ 1.png
            ... 
        ...
    ``` 
    Example
    ```python
    frame_dict = load_frames_from_folder("assets/player")
    my_sprite1 = Sprite(frame_dict)
    ```
    """
    return _load_frames_from_folder_uncached(folder_path)



def _load_frames_from_folder_uncached(folder_path: Union[Path, str]):
    
    def extract_images(path: Path):
        index2image: Dict[int, pygame.Surface] = {}

        for f in path.iterdir():
            if f.is_dir():
                continue

            if not f.stem.isdigit(): 
                print(f'skipping: {f.name}')
                continue
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

#RGBType = Tuple[int, int, int]
#RGBAType = Tuple[int, int, int, int]
#ColourType = Union[RGBAType, RGBType]

def create_circle(colour, radius: float) -> pygame.Surface:
    """
    Create a circle image (pygame.Surface) given the colour and radius. 

    Parameters
    ---
    colour: Tuple[int, int, int] or Tuple[int, int, int, int]
        The colour of the rectangle in RGB or RGBA. Value range: [0-255].
    radius: float
        the radius of the cirlce.
    """
    surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(surface, colour, (radius, radius), radius)
    return surface


def create_rect(colour, width: float, height: float) -> pygame.Surface:
    """
    Create a rectangle image (pygame.Surface) given the colour, width and height

    Parameters
    ---
    colour: Tuple[int, int, int] or Tuple[int, int, int, int]
        The colour of the rectangle in RGB or RGBA. Value range: [0-255].
    width: float
        the width (x length) of the rectangle.
    height: float
        the height (y length) of the rectangle.
    """

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, surface.get_rect())
    return surface

def scale_and_tile(image, screen_size, scale_factor):
    """
    Scale an image by a factor and tile it to fill the screen.
    
    THIS FUNCTION IS WRITTEN BY AN AI. 

    Parameters
    ----------
    image : pygame.Surface
        The image to scale and tile.
    screen_size : tuple of int
        The width and height of the target surface.
    scale_factor : float
        Factor by which to scale the image.
    """

    img_w, img_h = image.get_size()
    new_img = pygame.transform.smoothscale(image, (int(img_w * scale_factor), int(img_h * scale_factor)))
    new_img_w, new_img_h = new_img.get_size()
    
    tiled_surface = pygame.Surface(screen_size)
    
    for y in range(0, screen_size[1], new_img_h):
        for x in range(0, screen_size[0], new_img_w):
            tiled_surface.blit(new_img, (x, y))
    
    return tiled_surface


def scale_to_fill(image:pygame.Surface, new_size:Tuple[int, int]):
    """
    Scale an image to a new size without preserving aspect ratio.

    Parameters
    ----------
    image : pygame.Surface
        The image to scale.
    new_size : tuple of int
        Target width and height of the image.
    """
    return pygame.transform.smoothscale(image, new_size)


def scale_to_fit_aspect(image:pygame.Surface, new_size:Tuple[int, int], fit='horizontal'):
    """
    Scale an image to fit a rect while preserving aspect ratio.
    
    THIS FUNCTION IS WRITTEN BY AN AI. 

    Parameters
    ----------
    image : pygame.Surface
        The image to scale.
    new_size : tuple of int
        The width and height of the target rect.
    fit : 'horizontal' or 'vertical'
        Axis to fit the image against. Default is 'horizontal'.
    """
    img_rect = image.get_rect()
    screen_w, screen_h = new_size
    img_w, img_h = img_rect.size

    if fit == 'horizontal':
        scale_factor = screen_w / img_w
    elif fit == 'vertical':
        scale_factor = screen_h / img_h
    else:
        raise ValueError("fit must be either 'horizontal' or 'vertical'")

    new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
    return pygame.transform.smoothscale(image, new_size)


def _set_transparency(image, factor):
    """
    Set the transparency of an image.

    THIS FUNCTION IS WRITTEN BY AN AI. 

    ***IMCOMPLETE IMPLEMENTATION***: 
    The transparency of the transparent background of the image is also changed


    Parameters
    ----------
    image : pygame.Surface
        The image to adjust.
    factor : float
        Transparency level from 0.0 (fully transparent) to 1.0 (fully opaque).
    """
    new_image = image.copy()
    new_image.set_alpha(int(factor*255))
    return new_image

def set_transparency(image: pygame.Surface, factor):
    """
    Get a new copy of the image with the transparency applied.

    Parameters
    ----------
    image : pygame.Surface
        The image to adjust.
    factor : float
        Transparency level from 0.0 (fully transparent) to 1.0 (fully opaque).
    """
    w = image.get_width()
    h = image.get_height()

    sur = pygame.Surface((w, h)).convert_alpha()

    sur.fill((255,255,255,int(factor*255) ))
    #sur.set_alpha(int(factor*255))

    new_image = image.copy()
    new_image.blit(sur, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return new_image


def adjust_brightness(image, factor):
    """
    Get a new copy of the image with the brightness changes applied.
    
    THIS FUNCTION IS WRITTEN BY AN AI. 

    Parameters
    ----------
    image : pygame.Surface
        The image to adjust.
    factor : float
        Brightness multiplier. Values < 1.0 darken, values > 1.0 brighten.
       
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


def _draw_guide_lines(screen: pygame.Surface, font: pygame.font.Font, minor_grid, major_grid):
    w, h = screen.get_width(), screen.get_height()
    

    pygame.draw.lines(screen, (0,0,0), True, [(0,0), (0, h), (w, h), (w, 0)])
    screen.blit(font.render(f"({0},{0})", True, (0,0,0)), (5,5))
    for i in range(0, w, minor_grid):
        lw = 1
        v = 200
        if i and (not i % major_grid):
            lw = 1
            v = 0
            screen.blit(font.render(f"{i}", True, (0,0,0)), (i+5,5))

        pygame.draw.line(screen, (v,v,v,255-v), (i, 0), (i, h), width=lw)


        

    for i in range(0, h, minor_grid):
        lw = 1
        v = 200
        if i and (not i % major_grid):
            lw = 1
            v = 0
            screen.blit(font.render(f"{i}", True, (0,0,0)), (5,i+5))        
        pygame.draw.line(screen, (v,v,v,255-v), (0, i), (w, i), width=lw)

    #text = font.render(f"({w},{h})", True, (0,0,0))
    #screen.blit(text, (w-5-text.get_width(), h-5-text.get_height()))


    for x, y in product(range(major_grid, w, major_grid), range(major_grid, h, major_grid)):
        text = font.render(f"({x},{y})", True, (0,0,0))
        screen.blit(text, (x+5, y+5))



def _show_mouse_position(screen, font):
    w, h = screen.get_width(), screen.get_height()
    
    mx, my = pygame.mouse.get_pos()

    text = font.render(f"({mx},{my})", True, (0,0,0))
    screen.blit(text, (w-5-text.get_width(), h-5-text.get_height()))