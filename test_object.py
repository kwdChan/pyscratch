from scratch_sprite import ScratchSprite, circle_sprite, rect_sprite
import pygame
import pymunk
from game import game # neccessary for image loading

from helper import get_frame, get_frame_sequence, get_frame_dict
sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()

background = pygame.image.load('assets/kenney_fish-pack_2/Sample.png')
game.set_backdrops([background])


frame_dict = get_frame_dict(sprite_sheet, 2, 12, {
    "1": [0, 1], 
    "2": [2, 3],
    "3": [4, 5],
}, inset=0)


sprite_rect2 = rect_sprite((255, 240,240), 1000, 20, (400, 500))
game.add_sprite(sprite_rect2)
sprite_rect2.set_rotation(30)


sprite_rect = rect_sprite((255, 0,0), 100, 20, (500, 500))
game.add_sprite(sprite_rect)
sprite_rect.set_draggable(True)
sprite_rect.set_shape('box', 1, collision_allowed=True)


sprite_cir = circle_sprite((255, 0,0), 50, (100, 100), body_type=pymunk.Body.DYNAMIC)
sprite_cir.set_draggable(True)
sprite_cir.set_shape('circle', 1, collision_allowed=True)
game.add_sprite(sprite_cir)


sprite1 = ScratchSprite(frame_dict,  "1", (100,100), body_type=pymunk.Body.KINEMATIC)
sprite1.set_shape('box', shape_factor=.4)

sprite1.set_draggable(True)
game.add_sprite(sprite1)
game.set_gravity((0,0.002))
sprite1.scale_by(2)



sprite2 = ScratchSprite(frame_dict,  "1", (100,100), body_type=pymunk.Body.DYNAMIC)
sprite2.set_shape('box', shape_factor=.4, collision_allowed=True)
sprite1.scale_by(3)

#sprite1.set_scale(6)
sprite2.set_scale(4)

game.add_sprite(sprite2)


sprite1.lock_to(sprite2, (200,-200))

import random

# collision_event = Event.create_collision_event(sprite2, sprite1)
# collision_event.add_handler(lambda a: print(random.random()))


timer = game.create_timer_trigger(100)
timer.on_reset(lambda x: sprite1.next_frame())
#timer_event.add_handler(lambda: sprite1.add_rotation(3))
# timer_event.add_handler(lambda: sprite1.point_towards(sprite2))
# timer_event.add_handler(lambda: sprite1.point_towards_mouse())


game.retrieve_sprite_click_trigger(sprite2).add_callback(lambda: print('sprite2'))
game.retrieve_sprite_click_trigger(sprite1).add_callback(lambda: print('sprite1'))

game.create_collision_trigger(sprite2, sprite_cir).add_callback(lambda x: print('hi'))


timer2 = game.create_timer_trigger(500, 3)
timer2.on_reset(lambda x: sprite1.add_rotation(15))


game.create_conditional_trigger(lambda: pygame.mouse.get_pos()[0] < 100, 100).add_callback(lambda x: print(x))

keydown_event = game.create_pygame_event_trigger([pygame.KEYDOWN])
def when_key_down(e):

    
    if e.key == pygame.key.key_code("w"):
        # sprite1.move_indir(1)
        # sprite1.flip_horizontal()
        # #game.hide_sprite(sprite1)
        sprite2.body.velocity = sprite1.body.velocity[0], -1
        # game.move_to_back(sprite1)

    if e.key  == pygame.key.key_code("space"):
        #sprite1.body.velocity = sprite1.body.velocity[0], -.5
        game.create_timer_trigger(2000, 1).on_reset( lambda x: sprite1.scale_by(1.2))
        game.create_timer_trigger(3000, 1).on_reset( lambda x: sprite1.scale_by(1.2))

    elif e.key  == pygame.key.key_code("d"):
        sprite2.body.velocity = .5, sprite1.body.velocity[1]

    elif e.key  == pygame.key.key_code("a"):
        sprite2.body.velocity = -.5, sprite1.body.velocity[1]
        
    elif e.key  == pygame.key.key_code("1"):
        sprite1.set_frame_mode("1")
    elif e.key  == pygame.key.key_code("2"):
        sprite1.set_frame_mode("2")

    elif e.key  == pygame.key.key_code("3"):
        sprite1.set_frame_mode("3")

    elif e.key  == pygame.key.key_code("4"):
        game.switch_backdrop(0)
    elif e.key  == pygame.key.key_code("5"):
        game.next_backdrop()
    

keydown_event.add_callback(when_key_down)


game.create_edges()


game.start(60, sim_step_min=1000, debug_draw=False)

