import random
import re, sys
import numpy as np
import pymunk
from pyscratch import sensing
from pyscratch.scratch_sprite import ScratchSprite, create_rect, create_rect_sprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game
from main import *
from enemy import *

def game_start(data):

    player = create_rect_sprite((0, 0, 255), 50, 30, pos=(720//2, 1200))
    game.add_sprite(player)
    game.create_edges()
    player.set_collision_type(PLAYER_TYPE)


    healthbar_red = create_rect((255, 0, 0), 60, 50)

    healthbar_empty = create_rect_sprite((255, 255, 255), 60, 5, pos=(0,0))



    game.shared_data['player'] = player
    game.shared_data['inaccuracy'] = 5

    player.private_data['health'] = 10


    game.add_sprite(healthbar_empty)
    healthbar_empty.lock_to(player, (0,-30))
    healthbar_empty.blit(healthbar_red, (0,0))


    #game.create_timer_trigger(100, 20).on_reset(lambda x: create_bullet_move_sine((355, 1), 0))
    game.when_timer_reset(100, 20).on_reset(lambda x: create_bullet_attracted((355, 300)))
    #game.create_timer_trigger(100, 100).on_reset(lambda x: create_bullet_type1((100, 100), 90))

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



    game.when_timer_reset(1000/120).on_reset(run_forever)
    game.when_receive_message('player_health').add_callback(on_health_change)


game.when_timer_reset(0.1, 1).on_reset(game_start)