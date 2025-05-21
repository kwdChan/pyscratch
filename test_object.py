from scratch_sprite import ScratchSprite
from event import Event
import pygame
import pymunk
from game import game # neccessary for image loading
from helper import get_frame, get_frame_sequence, get_frame_dict
sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()


frame_dict = get_frame_dict(sprite_sheet, 2, 12, {
    "1": [0, 1], 
    "2": [2, 3],
})

sprite1 = ScratchSprite(frame_dict,  "1", (100,100), pymunk.Body.KINEMATIC)
game.add_sprite(sprite1)

sprite1.scale(4)

timer_event = Event.create_timer_event(.2)
timer_event.add_handler(sprite1.next_frame)


# # timer_event2 = Event.create_timer_event(0)
# # def test():
# #     sprite1.move_xy((1,2))

# timer_event2.add_handler(test)

    


keydown_event = Event.create_pygame_event(pygame.KEYDOWN)

def when_key_down(e):
    if e.key  == pygame.key.key_code("w"):
        sprite1.body.velocity = sprite1.body.velocity[0], -1    
    if e.key  == pygame.key.key_code("1"):
        sprite1.set_frame_mode("1")
    if e.key  == pygame.key.key_code("2"):
        sprite1.set_frame_mode("2")


keydown_event.add_handler(when_key_down)

