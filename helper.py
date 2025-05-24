import pygame
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

def adjust_brightness(surface, value):
    """Returns a new surface with brightness adjusted.
    
    Args:
        surface (pygame.Surface): The original surface.
        value (int or float): Amount to adjust brightness. Positive to brighten, negative to darken.
                              Can be an int (e.g., +50) or a multiplier (e.g., 1.2).
    
    Returns:
        pygame.Surface: New surface with adjusted brightness.


    WRITTEN BY CHATGPT
    """
    # Ensure we have a copy
    new_surface = surface.copy()

    # Convert to 24-bit or 32-bit format (RGB/RGBA)
    new_surface = new_surface.convert_alpha()

    # Get pixel arrays
    arr = pygame.surfarray.pixels3d(new_surface)
    
    # Brightness adjustment
    arr[...] = np.clip(arr * value, 0, 255)

    # Release the lock on the array (very important!)
    del arr

    return new_surface
