from pyscratch.scratch_sprite import ScratchSprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game
import pygame

game = Game()
sprite_sheet = pygame.image.load("assets/09493140a07b68502ef63ff423a6da3954d36fd8/Green Effect and Bullet 16x16.png").convert_alpha()

font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size

text_surface = font.render("Hello, Pygame!", True, (255, 255, 255))  # White text


frames = get_frame_dict(sprite_sheet, 36, 13, {
    "spin": [i+4*36 for i in range(14, 17+1)], 
    "star_explosion": [i+4*36 for i in range(19, 22+1)], 
    "heal": [i+1*36 for i in range(24, 28+1)], 
    "circle_explosion": [i+5*36 for i in range(14, 17+1)], 


    "square_bullets": [i+9*36 for i in range(24, 28+1)]+[i+9*36 for i in range(27, 24, -1)], 
    "circle_bullets": [i+8*36 for i in range(24, 28+1)]+[i+8*36 for i in range(27, 24, -1)], 

    "shield": [i+5*36 for i in [17]], 

    "bullet1": [i+3*36 for i in range(7, 7+1)]
})







bullet = ScratchSprite(frames, "bullet1", (400, 400))
bullet.set_scale(4)
game.add_sprite(bullet)
bullet.image.blit(text_surface, (0,0))



def on_key_press(k, updown):
    if updown == 'down':
        bullet.next_frame()
game.create_key_trigger().add_callback(on_key_press)

game.start(60, 60, False)