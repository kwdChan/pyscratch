

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
        if '.' in text and not text.startswith('.') and text.rfind('.') > 0:
            idx = text.rfind('.')
            return text[:idx], text[idx+1:]
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