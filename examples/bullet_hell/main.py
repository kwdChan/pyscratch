import random
import re, sys
import numpy as np
import pymunk
from pyscratch import sensing
from pyscratch.scratch_sprite import ScratchSprite, create_rect, rect_sprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game

from enemy import create_bullet_attracted, create_bullet_move_sine, create_bullet_start_pointing,create_bullet_type1

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



def game_start(data):

    player = rect_sprite((0, 0, 255), 50, 30, pos=(720//2, 1200))
    game.add_sprite(player)
    game.create_edges()
    player.set_collision_type(PLAYER_TYPE)


    healthbar_red = create_rect((255, 0, 0), 60, 50)

    healthbar_empty = rect_sprite((255, 255, 255), 60, 5, pos=(0,0))



    game.shared_data['player'] = player
    game.shared_data['inaccuracy'] = 5

    player.private_data['health'] = 10


    game.add_sprite(healthbar_empty)
    healthbar_empty.lock_to(player, (0,-30))
    healthbar_empty.blit(healthbar_red, (0,0))




    game.create_timer_trigger(100, 20).on_reset(lambda x: create_bullet_move_sine((355, 1), 0))
    game.create_timer_trigger(100, 20).on_reset(lambda x: create_bullet_attracted((355, 1)))
    game.create_timer_trigger(100, 100).on_reset(lambda x: create_bullet_type1((100, 100), 90))

    #game.create_timer_trigger(100, 10)
    
    
    #game.create_timer_trigger(1200).on_reset(lambda x: shoot_player_bullet((player.x, player.y), game.shared_data['inaccuracy']))
    #game.create_timer_trigger(500, 30).on_reset(lambda x: create_enemy_type1((random.random()*WIDTH, 0)))


    def run_forever(_):
        if sensing.is_key_pressed(['w']):
            player.move_xy((0, -5))

        if sensing.is_key_pressed(['s']):
            player.move_xy((0, 5))

        if sensing.is_key_pressed(['a']):
            player.move_xy((-5, 0))

        if sensing.is_key_pressed(['d']):
            player.move_xy((5, 0))

        player.set_xy((cap(player.x, 50, WIDTH-50), cap(player.y, HEIGHT-500, HEIGHT)))

        
    def on_health_change(change):
        player.private_data['health'] += change
        new_health = max(0, player.private_data['health'])

        healthbar_red = create_rect((255, 0, 0), 60*(new_health/10), 50)
        healthbar_empty.blit(healthbar_red)



    game.create_timer_trigger(1000/120).on_reset(run_forever)
    game.create_messager_trigger('player_health').add_callback(on_health_change)


game_start(None)
game.start(60, 300, False)
