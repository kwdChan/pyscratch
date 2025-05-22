from scratch_sprite import ScratchSprite, circle_sprite, rect_sprite
from event import Event
import pygame
import pymunk
from game import game # neccessary for image loading

from helper import get_frame, get_frame_sequence, get_frame_dict
sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()


frame_dict = get_frame_dict(sprite_sheet, 2, 12, {
    "1": [0, 1], 
    "2": [2, 3],
}, inset=0)

sprite3 = rect_sprite((255, 0,0), 100, 20, (500, 500))
game.add_sprite(sprite3)

sprite3.set_draggable(True)
sprite2 = circle_sprite((255, 0,0), 50, (100, 100), body_type=pymunk.Body.DYNAMIC)
game.add_sprite(sprite2)
print(sprite2.rect)

sprite2.set_shape('box', 1)
print(sprite2.rect)
sprite1 = ScratchSprite(frame_dict,  "1", (100,100), body_type=pymunk.Body.KINEMATIC)

sprite1.set_shape('box', shape_factor=.4)
game.add_sprite(sprite1)
import random

collision_event = Event.create_collision_event(sprite2, sprite1)
collision_event.add_handler(lambda a: print(random.random()))




# overlap_event = Event.create_overlap_event(sprite2, sprite1)
# overlap_event.add_handler(lambda: print(random.random()))

sprite1.scale(4)

timer_event = Event.create_timer_event(.1)
timer_event.add_handler(lambda: sprite1.add_rotation(3))
timer_event.add_handler(lambda: sprite1.next_frame())


# # timer_event2 = Event.create_timer_event(0)
# # def test():
# #     sprite1.move_xy((1,2))

# timer_event2.add_handler(test)

    


keydown_event = Event.create_pygame_event([pygame.KEYDOWN])

def when_key_down(e):
    if e.key  == pygame.key.key_code("w"):
        #sprite1.body.velocity = sprite1.body.velocity[0], -.5
        game.schedule_job(2, lambda: sprite1.scale(1.2))
        game.schedule_job(3, lambda: sprite1.scale(1.2))

    elif e.key  == pygame.key.key_code("d"):
        sprite1.body.velocity = .5, sprite1.body.velocity[1]

    elif e.key  == pygame.key.key_code("a"):
        sprite1.body.velocity = -.5, sprite1.body.velocity[1]
        
    elif e.key  == pygame.key.key_code("1"):
        sprite1.set_frame_mode("1")
    elif e.key  == pygame.key.key_code("2"):
        sprite1.set_frame_mode("2")


keydown_event.add_handler(when_key_down)

