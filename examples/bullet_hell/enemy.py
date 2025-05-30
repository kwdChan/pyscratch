import pyscratch as pysc
import random
from setting import *
from enemy_bullets import *

def spawn_line(_):
    n = 10
    margin = 20
    itv = (SCREEN_WIDTH-margin*2)//(n-1)
    y=0
    for i in range(n):

        x = itv*i+margin

        create_standard_enemy((x, y), 90, False, False, 5, 1000)


def spawn_6_side_entry(_):

    pos1 = (0, 200)
    pos2 = (0, 400)
    pos3 = (0, 600)

    pos4 = (SCREEN_WIDTH, 200)
    pos5 = (SCREEN_WIDTH, 400)
    pos6 = (SCREEN_WIDTH, 600)


    create_standard_enemy(pos1, 45, True, False, 5)
    create_standard_enemy(pos2, 45, True, False, 5)
    create_standard_enemy(pos3, 45, True, False, 5)


    create_standard_enemy(pos4, 90+45, True, False, 5)
    create_standard_enemy(pos5, 90+45, True, False, 5)
    create_standard_enemy(pos6, 90+45,True,  False, 5)






def spawn_random(_):
    pos = pysc.helper.random_number(0, SCREEN_WIDTH), 0
    speed = pysc.helper.random_number(1, 10)
    rotation = pysc.helper.random_number(90-10, 90+10)

    create_standard_enemy(pos, rotation, False, False, speed)
    

def spawn_kamikaze(_):
    pos = pysc.helper.random_number(0, SCREEN_WIDTH), 0
    speed = pysc.helper.random_number(7, 12)

    create_standard_enemy(pos, 90, False, True, speed, bullet_period=1000000)
    


def create_standard_enemy(position, rotation, start_point, pointing_to_player, speed, bullet_period=150):

    

    # create the sprite
    enemy_sprite = pysc.rect_sprite((255, 0, 0), 50, 30, pos=position)
    pysc.game.add_sprite(enemy_sprite)
    enemy_sprite.set_collision_type(ENEMY_TYPE)

    enemy_sprite.add_rotation(rotation)

    if start_point:
        enemy_sprite.point_towards_sprite(pysc.game.shared_data['player'])
        

    # behaviour
    ## 1. move a straight line
    ## 2. shoot bullets (of type based on the level) at a constant interval (based on the level)
    ## 3. hitting a player 
    ## 4. hit by player buller
    ## 5. destroyed when leaving the screen


    ## 1. move a straight line   
    movement_event = pysc.game.create_timer_trigger(20)
    movement_event.on_reset(lambda x: enemy_sprite.move_indir(speed))

    if pointing_to_player: 
        movement_event.on_reset(
            lambda x: enemy_sprite.point_towards_sprite(pysc.game.shared_data['player'])
        )


    ## 2. shoot bullets (of type based on the level) at a constant interval (based on the level)
    bullet_event = pysc.game.create_timer_trigger(bullet_period).on_reset(lambda x: create_straight_bullet((enemy_sprite.x, enemy_sprite.y), enemy_sprite.get_rotation()))


    ## 3. hitting a player
    when_hit_player = pysc.game.create_conditional_trigger(lambda: pysc.sensing.is_touching(pysc.game, enemy_sprite, pysc.game.shared_data['player']), repeats=1)
    when_hit_player.add_callback(lambda x: pysc.game.boardcast_message('player_health', -1))

    ## 4. hit by player buller
    when_hit_by_player_bullet = pysc.game.create_type2type_collision_trigger(PLAYER_BULLET_TYPE, ENEMY_TYPE)
    
    ## 5. destroyed when leaving the screen
    when_leaving_screen =pysc.game.create_conditional_trigger(lambda: (enemy_sprite.y > SCREEN_HEIGHT), repeats=1)

    ### callback for 3, 4, 5
    def destroy(x):
        movement_event.remove()
        bullet_event.remove()
        when_hit_player.remove()
        when_hit_by_player_bullet.remove()
        when_leaving_screen.remove()
        pysc.game.remove_sprite(enemy_sprite)

    def check_collision(a):
        if enemy_sprite.shape in a.shapes:
            destroy(None)
    
    when_hit_by_player_bullet.add_callback(check_collision)
    when_hit_player.add_callback(destroy)
    when_leaving_screen.add_callback(destroy)


# testing only
pysc.game.create_timer_trigger(500, 20).on_reset(spawn_random)


pysc.game.create_timer_trigger(3000, 1).on_reset(spawn_6_side_entry)
pysc.game.create_timer_trigger(2000, 1).on_reset(spawn_line)


