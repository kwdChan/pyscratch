from scratch_sprite import ScratchSprite
from event import Event
import pygame
import pymunk
from game import game # neccessary for image loading

sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()

def get_frame(sheet, frame_width, frame_height, frame_index, row=0):
    frame_rect = pygame.Rect(frame_index * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(frame_rect)
    return frame


sprite1 = ScratchSprite([get_frame(sprite_sheet, 48, 48, 1, row=i) for i in range(4)], (100,100), pymunk.Body.DYNAMIC)
game.add_sprite(sprite1)



#timer_event = Event.create_timer_event(2)
#timer_event.add_handler(sprite1.next_frame)

# # timer_event2 = Event.create_timer_event(0)
# # def test():
# #     sprite1.move_xy((1,2))

# timer_event2.add_handler(test)

    


keydown_event = Event.create_pygame_event(pygame.KEYDOWN)

def when_key_down(e):
    if e.key  == pygame.key.key_code("w"):
        sprite1.body.velocity = sprite1.body.velocity[0], -1    
    if e.key  == pygame.key.key_code("s"):
        sprite1.scale(2)
keydown_event.add_handler(when_key_down)

