import pygame
import pyscratch as pysc

sheet = pygame.image.load("assets/kenney_fish-pack_2/Spritesheet/spritesheet-double.png").convert_alpha()
pysc.helper.cut_sprite_sheet(
    sheet, 
    11, 12, 
    folder_path='examples/getting-started/assets/'
)

