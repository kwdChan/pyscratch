import random
import re, sys
import numpy as np
import pymunk
from pyscratch import sensing
from pyscratch.sprite import Sprite, create_rect, create_rect_sprite, create_edge_sprites
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game
import pygame
WIDTH = 720
HEIGHT = 1280


ENEMY_TYPE = 3
PLAYER_TYPE = 2
PLAYER_BULLET_TYPE = 4
EDGE_TYPE = 1

def cap(v, min_v, max_v):
    return max(min(max_v, v), min_v)



game = Game((WIDTH, HEIGHT))
sprite_sheet = pygame.image.load("assets/09493140a07b68502ef63ff423a6da3954d36fd8/Green Effect and Bullet 16x16.png").convert_alpha()

font = pygame.font.SysFont(None, 24)  # None = default font, 48 = font size
game.suppress_type_collision(PLAYER_TYPE, True)


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



start_buttom = create_rect_sprite((200, 0, 0), width=150, height=60, pos=(game._screen.get_width()//2, game._screen.get_height()//2))
start_buttom.write_text("Click to Start", font)
#game.add_sprite(start_buttom)

def on_click():
    start_buttom.scale_by(0.9)

    on_condition = game.when_condition_met(
        lambda: (not sensing.get_mouse_presses()[0]), repeats=1)
    
    def start_game(x):
        start_buttom.scale_by(1/0.9)
        game.broadcast_message('game_start', {'count': 0})
        game.remove_sprite(start_buttom)

    on_condition.add_handler(start_game)

#game.retrieve_sprite_click_trigger(start_buttom).add_callback(on_click)
on_click()


def shoot_player_bullet(origin, inaccuracy):

    bullet = Sprite(frames, "circle_bullets", origin)

    #game.add_sprite(bullet)
    bullet.set_collision_type(PLAYER_BULLET_TYPE)
    bullet.set_rotation(-90 + inaccuracy*random.random()-inaccuracy/2)

    movement_timer = game.when_timer_reset(1000/240).add_handler(
        lambda x: bullet.move_indir(2)
    )

    next_frame_timer = game.when_timer_reset(100).add_handler(
        lambda x: bullet.next_frame()
    )


    def destroy_when_exit(x):
        movement_timer.remove()
        next_frame_timer.remove()
        game.remove_sprite(bullet)


    destroy_condition = game.when_condition_met(lambda: (bullet.y < 0), repeats=1)
    destroy_condition.add_handler(destroy_when_exit)


def create_bullet_attracted(position):
    bullet = Sprite(frames, "spin", position)
    
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5


    movement_event = game.when_timer_reset(20).add_handler(lambda x: bullet.move_indir(speed))
    following_event = game.when_timer_reset(200, 5).add_handler(lambda x: bullet.point_towards_sprite(game.shared_data['player']))

    frame_event = game.when_timer_reset(200).add_handler(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_handler(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        following_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)
    when_exit_screen.add_handler(destory)
    hitting_player_event.add_handler(explode_and_destroy)



def create_bullet_start_pointing(position, _):

    bullet = Sprite(frames, "spin", position)

    

    bullet.point_towards_sprite(game.shared_data['player'])
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5
    bullet.point_towards_sprite(game.shared_data['player'])


    movement_event = game.when_timer_reset(20).add_handler(lambda x: bullet.move_indir(speed))
    #movement_event = game.create_timer_trigger(20).on_reset(lambda x: bullet.move_across_dir((random.random()-0.5)*speed*0.3))


    frame_event = game.when_timer_reset(200).add_handler(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_handler(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)
    when_exit_screen.add_handler(destory)
    hitting_player_event.add_handler(explode_and_destroy)
    pass




def create_bullet_move_sine(position, rotation):
    bullet = Sprite(frames, "square_bullets", position)
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

    
    movement_event.add_handler(move)


    frame_event = game.when_timer_reset(200).add_handler(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_handler(destory)


    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)

    when_exit_screen = game.when_condition_met(lambda: (bullet.y > HEIGHT) or (bullet.y < 0) or (bullet.x <0) or (bullet.x>WIDTH) , repeats=1)
    when_exit_screen.add_handler(destory)
    hitting_player_event.add_handler(explode_and_destroy)




def create_bullet_type1(position, rotation):
    bullet = Sprite(frames, "spin", position)
    bullet.add_rotation(rotation)
    bullet.set_scale(2.3)
    #game.add_sprite(bullet)
    speed = random.random()*15+5
    #speed = 15

    movement_event = game.when_timer_reset(20).add_handler(lambda x: bullet.move_indir(speed))
    #movement_event = game.create_timer_trigger(20).on_reset(lambda x: bullet.move_across_dir((random.random()-0.5)*speed*0.3))


    frame_event = game.when_timer_reset(200).add_handler(lambda x: bullet.next_frame())
    hitting_player_event = game.create_specific_collision_trigger(bullet, game.shared_data['player'])

    
    def explode_and_destroy(a):
        bullet.set_frame_mode('star_explosion')
        game.broadcast_message('player_health', -1)
        movement_event.remove()
        game.when_timer_reset(200, 1).add_handler(destory)

    when_exit_screen = game.when_condition_met(lambda: bullet.y > HEIGHT, repeats=1)

    def destory(x):
        movement_event.remove()
        frame_event.remove()
        hitting_player_event.remove()
        game.remove_sprite(bullet)
        when_exit_screen.remove()

    when_exit_screen.add_handler(destory)
    hitting_player_event.add_handler(explode_and_destroy)






def create_enemy_type1(position):

    enemy_sprite = create_rect_sprite((255, 0, 0), 50, 30, pos=position)
    #game.add_sprite(enemy_sprite)

    enemy_sprite.add_rotation(90+(random.random()-0.5)*15)
    enemy_sprite.set_collision_type(ENEMY_TYPE)


    speed = random.random()*6




    movement_event = game.when_timer_reset(20).add_handler(lambda x: enemy_sprite.move_indir(speed))
    bullet_event = game.when_timer_reset(150).add_handler(lambda x: create_bullet_type1((enemy_sprite.x, enemy_sprite.y), enemy_sprite.get_rotation()))
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

    when_hit_player.add_handler(destroy)
    when_hit_player.add_handler(lambda x: game.broadcast_message('player_health', -1))
    
    when_leaving_screen.add_handler(destroy)

    when_hit_by_player_bullet.add_handler(check_collision)






def game_start(data):

    player = create_rect_sprite((0, 0, 255), 50, 30, pos=(720//2, 1200))
    #game.add_sprite(player)
    create_edge_sprites(game)
    player.set_collision_type(PLAYER_TYPE)


    healthbar_red = create_rect((255, 0, 0), 60, 50)

    healthbar_empty = create_rect_sprite((255, 255, 255), 60, 5, pos=(0,0))



    game.shared_data['player'] = player
    game.shared_data['inaccuracy'] = 5

    player.private_data['health'] = 10


    #game.add_sprite(healthbar_empty)
    healthbar_empty.lock_to(player, (0,-30))
    healthbar_empty.blit(healthbar_red, (0,0))




    game.when_timer_reset(100, 20).add_handler(lambda x: create_bullet_move_sine((355, 1), 0))
    game.when_timer_reset(100, 20).add_handler(lambda x: create_bullet_attracted((355, 1)))
    game.when_timer_reset(100, 100).add_handler(lambda x: create_bullet_type1((100, 100), 90))

    #game.create_timer_trigger(100, 10)
    
    
    #game.create_timer_trigger(1200).on_reset(lambda x: shoot_player_bullet((player.x, player.y), game.shared_data['inaccuracy']))
    #game.create_timer_trigger(500, 30).on_reset(lambda x: create_enemy_type1((random.random()*WIDTH, 0)))


    def run_forever(_):
        if sensing.is_key_pressed('w'):
            player.move_xy((0, -5))

        if sensing.is_key_pressed('s'):
            player.move_xy((0, 5))

        if sensing.is_key_pressed('a'):
            player.move_xy((-5, 0))

        if sensing.is_key_pressed('d'):
            player.move_xy((5, 0))

        player.set_xy((cap(player.x, 50, WIDTH-50), cap(player.y, HEIGHT-500, HEIGHT)))

        
    def on_health_change(change):
        player.private_data['health'] += change
        new_health = max(0, player.private_data['health'])

        healthbar_red = create_rect((255, 0, 0), 60*(new_health/10), 50)
        healthbar_empty.blit(healthbar_red)



    game.when_timer_reset(1000/120).add_handler(run_forever)
    game.when_receive_message('player_health').add_handler(on_health_change)

wait_for_game_start = game.when_receive_message('game_start').add_handler(game_start)


game.start(60, 60, False, True)
