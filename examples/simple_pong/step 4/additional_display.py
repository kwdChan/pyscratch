import pyscratch as pysc
import pygame
font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size
pysc.create_shared_data_display_sprite('left_score', font, size=(300, 60))
