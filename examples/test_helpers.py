import pyscratch as pysc
import pygame


#sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()

#pysc.helper.save_frame_from_sprite_sheet(sprite_sheet, 2, 12, folder_path='assets/cat')


x = pysc.create_single_costume_sprite('assets/cat/hi/0.png')

def forever():
    x.set_frame_mode('hi2')
    while True: 
        x.next_frame()

        yield 100

x.when_game_start().add_callback(forever)
pysc.game.start(60)