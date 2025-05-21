import pygame



def get_frame(sheet, columns, rows, index):
    sheet_rect = sheet.get_rect()
    frame_width = sheet_rect.width // columns
    frame_height = sheet_rect.height // rows

    # Calculate x (column) and y (row) from index
    col = index % columns
    row = index // columns

    frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(frame_rect)
    return frame


def get_frame_sequence(sheet, columns, rows, indices):
    return [get_frame(sheet, columns, rows, i) for i in indices]

def get_frame_dict(sheet, columns, rows, indices_dict):
    frame_dict = {}
    for k, v in indices_dict.items():
        assert isinstance(v, list) or isinstance(v, tuple)

        frame_dict[k] = get_frame_sequence(sheet, columns, rows, v)

    return frame_dict