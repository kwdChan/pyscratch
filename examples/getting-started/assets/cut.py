import pygame
import pyscratch as pysc

sheet = pygame.image.load("assets/kenney_fish-pack_2/Spritesheet/spritesheet-double.png").convert_alpha()
pysc.helper.save_frame_from_sprite_sheet(
    sheet, 
    11, 12, 
    folder_path='examples/getting-started/assets/'
)

