from pathlib import Path
from typing import Tuple
import pyscratch as pysc
from settings import *

width, height = 100, 140
colour = (130, 130, 130)

spacing = 10
n_cols = 6

def try_load_image(path):
    try: 
        return pysc.load_image(path)
    except:
        return None


import pygame
import pygame

def render_wrapped_file_name(text, max_chars, font, color=(255, 255, 255), bg_color=None, max_lines=None):
    """
    THIS FUNCTION IS WRITTEN BY AN AI

    Renders a file name like a file explorer: wrapping intelligently while preserving the extension.

    :param text: The file name string to render.
    :param max_chars: Maximum number of characters per line (approximate width).
    :param font: Pygame font object to render with.
    :param color: Text color (default white).
    :param bg_color: Background color (default None = transparent).
    :param max_lines: Optional maximum number of lines to render. Extra text will be truncated with '...'.
    :return: A Pygame surface with the rendered multiline text.
    """
    def split_file_name(text):
        if '.' in text:
            parts = text.split('.')
            ext = parts[-1]
            base = '.'.join(parts[:-1])
            return base, ext
        else:
            return text, ''

    def wrap_lines(base, ext, max_chars, max_lines=None):
        words = base.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = (current_line + ' ' + word).strip()
            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    if max_lines and len(lines) == max_lines:
                        return lines[:-1] + [truncate_with_ellipsis(current_line, max_chars)]
                # Break long word
                while len(word) > max_chars:
                    lines.append(word[:max_chars])
                    word = word[max_chars:]
                    if max_lines and len(lines) == max_lines:
                        return lines[:-1] + [truncate_with_ellipsis(lines[-1], max_chars)]
                current_line = word

        if current_line:
            lines.append(current_line)
            if max_lines and len(lines) > max_lines:
                lines = lines[:max_lines]
                lines[-1] = truncate_with_ellipsis(lines[-1], max_chars)

        # Add extension
        if ext:
            if len(lines[-1] + '.' + ext) <= max_chars:
                lines[-1] += '.' + ext
            elif not max_lines or len(lines) < max_lines:
                lines.append('.' + ext)
            else:
                lines[-1] = truncate_with_ellipsis(lines[-1], max_chars)

        return lines

    def truncate_with_ellipsis(line, max_chars):
        return line[:max(0, max_chars - 3)] + '...'

    # Prepare
    base, ext = split_file_name(text)
    lines = wrap_lines(base, ext, max_chars, max_lines)

    # Render
    line_height = font.get_linesize()
    surface_height = line_height * len(lines)
    surface_width = max(font.size(line)[0] for line in lines)

    rendered_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
    if bg_color:
        rendered_surface.fill(bg_color)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        rendered_surface.blit(text_surface, (0, i * line_height))

    return rendered_surface




def FileDisplay(path: Path, order: int, panel_top_left):
    sprite = pysc.create_rect_sprite(colour, width, height)
    
    # set the position

    panel_x, panel_y = panel_top_left
    sprite.x = spacing+(order%n_cols)*(width+spacing)+panel_x +width/2
    sprite.y = spacing+(order//n_cols)*(height+spacing)+panel_y +height/2

    # set the display

    surface = try_load_image(path)
    if not surface: 
        # TODO: messy af
        if path.is_file():
            sprite.remove()
            return None
        
        text = render_wrapped_file_name(path.name+'/', 8, DEFAULT_FONT24)
        sprite.draw(text, offset=(width/2, height/2) )
        #sprite.write_text(path.name+'/', DEFAULT_FONT24, offset=(width/2, height/2))
        
    else: 
        image_margin = 20
        text_height = 20
        fit = "horizontal" if surface.get_width() >= surface.get_height() else "vertical"
        surface = pysc.scale_to_fit_aspect(surface, (width-image_margin, height-text_height-image_margin ), fit)
        sprite.draw(surface, (width/2, (height-text_height)/2))
        
        text = render_wrapped_file_name(path.name, 8, DEFAULT_FONT24, color= (0, 0, 0), max_lines=2)
        sprite.draw(text,offset=(width/2, height-20), reset=False)



    sprite.private_data['is_file'] = path.is_file()


    def on_click():
        if not path.is_file():
            pysc.game.broadcast_message('folder_update', path)
        else:
            pysc.game.broadcast_message('image_selected', path)
            #pysc.game.broadcast_message('cut_or_nav_mode_change', 'cut')



    sprite.when_this_sprite_clicked().add_handler(on_click)


    def on_msg_mode_change(mode):
        if mode == 'nav':
            sprite.show()
            #pysc.game.bring_to_front(sprite)
        else:
            sprite.hide()

    sprite.when_receive_message('cut_or_nav_mode_change').add_handler(on_msg_mode_change)




    return sprite
    
