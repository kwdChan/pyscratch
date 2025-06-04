import random
import re, sys
import numpy as np
import pymunk
from pyscratch import sensing
from pyscratch.scratch_sprite import ScratchSprite, create_rect, create_rect_sprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game

from main import game, frames, WIDTH, HEIGHT, ENEMY_TYPE, PLAYER_BULLET_TYPE


def create_bullet_attracted(position):
    bullet = ScratchSprite(frames, "spin", position)
    
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5

    bullet.point_towards_sprite(game.shared_data['player'])


    movement_event = game.when_timer_reset(20).add_callback(lambda x: bullet.move_indir(speed))
    following_event = game.when_timer_reset(200, 5).add_callback(lambda x: bullet.point_towards_sprite(game.shared_data['player']))

    frame_event = game.when_timer_reset(200).add_callback(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_callback(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        following_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)
    when_exit_screen.add_callback(destory)
    hitting_player_event.add_callback(explode_and_destroy)



def create_bullet_start_pointing(position, _):

    bullet = ScratchSprite(frames, "spin", position)

    

    bullet.point_towards_sprite(game.shared_data['player'])
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5
    bullet.point_towards_sprite(game.shared_data['player'])


    movement_event = game.when_timer_reset(20).add_callback(lambda x: bullet.move_indir(speed))
    #movement_event = game.create_timer_trigger(20).on_reset(lambda x: bullet.move_across_dir((random.random()-0.5)*speed*0.3))


    frame_event = game.when_timer_reset(200).add_callback(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_callback(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)
    when_exit_screen.add_callback(destory)
    hitting_player_event.add_callback(explode_and_destroy)
    pass




def create_bullet_move_sine(position, rotation):
    bullet = ScratchSprite(frames, "square_bullets", position)
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    bullet.set_rotation(rotation+90)
    #speed = random.random()*15+5
    speed = 10


    bullet.private_data['phase'] = 0
    movement_event = game.when_timer_reset(30)
    def move(x):
        bullet.private_data['phase']+=.1
        angle = np.tanh(np.cos(.6*bullet.private_data['phase']))


        bullet.add_rotation(angle)
                            
        bullet.move_indir(speed)

    
    movement_event.add_callback(move)


    frame_event = game.when_timer_reset(200).add_callback(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_callback(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: (bullet.y > HEIGHT) or (bullet.y < 0) or (bullet.x <0) or (bullet.x>WIDTH) , repeats=1)
    when_exit_screen.add_callback(destory)
    hitting_player_event.add_callback(explode_and_destroy)




def create_bullet_type1(position, rotation):
    bullet = ScratchSprite(frames, "spin", position)
    bullet.add_rotation(rotation)
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5
    #speed = 15

    movement_event = game.when_timer_reset(20).add_callback(lambda x: bullet.move_indir(speed))
    #movement_event = game.create_timer_trigger(20).on_reset(lambda x: bullet.move_across_dir((random.random()-0.5)*speed*0.3))


    frame_event = game.when_timer_reset(200).add_callback(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_callback(destory)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)

    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)
        when_exit_screen.remove()

    when_exit_screen.add_callback(destory)
    hitting_player_event.add_callback(explode_and_destroy)






def create_enemy_type1(position):

    enemy_sprite = create_rect_sprite((255, 0, 0), 50, 30, pos=position)
    #game.add_sprite(enemy_sprite)

    enemy_sprite.add_rotation(90+(random.random()-0.5)*15)
    enemy_sprite.set_collision_type(ENEMY_TYPE)


    speed = random.random()*6
    print(game.shared_data['player'])



    movement_event = game.when_timer_reset(20).add_callback(lambda x: enemy_sprite.move_indir(speed))
    bullet_event = game.when_timer_reset(150).add_callback(lambda x: create_bullet_type1((enemy_sprite.x, enemy_sprite.y), enemy_sprite.get_rotation()))
    #bullet_event = game.create_timer_trigger(1500).on_reset(lambda x: create_bullet_attracted((enemy_sprite.x, enemy_sprite.y)))

    when_hit_player = game.when_condition_met(lambda: sensing.is_touching(game, enemy_sprite, game.shared_data['player']), repeats=1)
    when_leaving_screen = game.when_condition_met(lambda: (enemy_sprite.y > HEIGHT), repeats=1)
    when_hit_by_player_bullet = game.create_type2type_collision_trigger(PLAYER_BULLET_TYPE, ENEMY_TYPE)


    


    def destroy(x):
        when_hit_player.remove()
        when_leaving_screen.remove()
        when_hit_by_player_bullet.remove()
        movement_event.remove()
        bullet_event.remove()
        game.remove_sprite(enemy_sprite)

    def check_collision(a):
        if enemy_sprite.shape in a.shapes:
            destroy(None)

    when_hit_player.add_callback(destroy)
    when_hit_player.add_callback(lambda x: game.broadcast_message('player_health', -1))
    
    when_leaving_screen.add_callback(destroy)

    when_hit_by_player_bullet.add_callback(check_collision)


    

