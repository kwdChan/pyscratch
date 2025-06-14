from pyscratch.sprite import Sprite, create_circle_sprite, create_rect_sprite
import pygame
import pymunk
from pyscratch.game import game # neccessary for image loading
from pyscratch.helper import scale_to_fit_aspect, scale_and_tile, scale_to_fill_screen, adjust_brightness, set_transparency

from pyscratch.helper import get_frame, get_frame_sequence, get_frame_dict

game.update_screen_mode((2300, 700))
sprite_sheet = pygame.image.load("assets/Sprout Lands - Sprites - Basic pack/Characters/Basic Charakter Actions.png").convert_alpha()

background = pygame.image.load('assets/kenney_fish-pack_2/Sample.png').convert() # TODO: convert is needed 
#background = scale_to_fit_aspect(background, game.screen.get_size())
background = scale_to_fill_screen(background, game._screen.get_size())
#background = scale_and_tile(background, game.screen.get_size(), 0.5)


#background = adjust_brightness(background, 0.9)
background = set_transparency(background, .5)


game.set_backdrops([background])

game.load_sound('bong', 'assets/sound_effects/Metal Clang-SoundBible.com-19572601.wav')




frame_dict = get_frame_dict(sprite_sheet, 2, 12, {
    "1": [0, 1], 
    "2": [2, 3],
    "3": [4, 5],
}, inset=0)


sprite_rect2 = create_rect_sprite((255, 240,240), 1000, 20, (400, 500))
game._add_sprite(sprite_rect2)
sprite_rect2.set_rotation(30)


sprite_rect = create_rect_sprite((255, 0,0), 100, 20, (500, 500))
game._add_sprite(sprite_rect)
sprite_rect.set_draggable(True)
sprite_rect.set_shape('box', 1, collision_allowed=True)


sprite_cir = create_circle_sprite((255, 0,0), 50, (100, 100), body_type=pymunk.Body.DYNAMIC)
sprite_cir.set_draggable(True)
sprite_cir.set_shape('circle', 1, collision_allowed=True)
game._add_sprite(sprite_cir)


sprite1 = Sprite(frame_dict,  "1", (100,100), body_type=pymunk.Body.KINEMATIC)
sprite1.set_shape('box', shape_factor=.4)

sprite1.set_draggable(True)
game._add_sprite(sprite1)
game.set_gravity((0,0.002))
sprite1.scale_by(2)



sprite2 = Sprite(frame_dict,  "1", (100,100), body_type=pymunk.Body.DYNAMIC)
sprite2.set_shape('box', shape_factor=.4, collision_allowed=True)
sprite1.scale_by(3)

#sprite1.set_scale(6)
sprite2.set_scale(4)

game._add_sprite(sprite2)


sprite1.lock_to(sprite2, (200,-200))

import random




timer = game.when_timer_reset(100)
timer.add_handler(lambda x: sprite1.next_frame())
#timer_event.add_handler(lambda: sprite1.add_rotation(3))
# timer_event.add_handler(lambda: sprite1.point_towards(sprite2))
# timer_event.add_handler(lambda: sprite1.point_towards_mouse())


game.when_this_sprite_clicked(sprite2).add_handler(lambda: print('sprite2'))
game.when_this_sprite_clicked(sprite1).add_handler(lambda: print('sprite1'))

game.create_specific_collision_trigger(sprite2, sprite_cir).add_handler(lambda x: game.play_sound('bong', 0.2))


timer2 = game.when_timer_reset(500, 3)
timer2.add_handler(lambda x: sprite1.add_rotation(15))


game.when_condition_met(lambda: pygame.mouse.get_pos()[0] < 100, 100).add_handler(lambda x: print(x))


hello_word_trigger = game.when_receive_message('hello_world')
hello_word_trigger.add_handler(lambda x: print(x))

simple_key_event = game.when_any_key_pressed()

def on_key_press(key, updown):
    game.broadcast_message('hello_world', dict(x=key))
    print(game._all_message_subscriptions)


    
simple_key_event.add_handler(on_key_press)



keydown_event = game.create_pygame_event_trigger([pygame.KEYDOWN])



def when_key_down(e):

    
    if e.key == pygame.key.key_code("w"):
        hello_word_trigger.remove()
        # sprite1.move_indir(1)
        # sprite1.flip_horizontal()
        # #game.hide_sprite(sprite1)
        sprite2.body.velocity = sprite1.body.velocity[0], -1
        # game.move_to_back(sprite1)

    if e.key  == pygame.key.key_code("space"):
        #sprite1.body.velocity = sprite1.body.velocity[0], -.5
        #sprite1.set_brightness(1.1)
        sprite1.set_transparency(.1)
        sprite2.body.moment = 1
        sprite2.body.mass = .1
        #game.create_timer_trigger(2000, 1).on_reset( lambda x: sprite1.scale_by(1.2))
        #game.create_timer_trigger(3000, 1).on_reset( lambda x: sprite1.scale_by(1.2))

    elif e.key  == pygame.key.key_code("d"):
        sprite2.body.velocity = .5, sprite1.body.velocity[1]
    elif e.key  == pygame.key.key_code("s"):
        sprite2.scale_by(1.4)
        
        
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

    elif e.key  == pygame.key.key_code("6"):
        keydown_event.remove()

keydown_event.add_handler(when_key_down)

game.remove_sprite(sprite1)
#game.all_sprites.remove(sprite1)

game.create_edges()
game.backdrop_change_trigger.add_callback(lambda x: print(x))

game.start(60, sim_step_min=1000, debug_draw=True)

