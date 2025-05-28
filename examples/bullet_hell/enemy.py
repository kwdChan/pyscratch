import pyscratch as pysc
import random
from setting import *



def create_enemy_type1(_):



    enemy_sprite = pysc.rect_sprite((255, 0, 0), 50, 30, pos=(pysc.helper.random_number(0, SCREEN_WIDTH), 0))
    pysc.game.add_sprite(enemy_sprite)

    enemy_sprite.add_rotation(90+(random.random()-0.5)*15)
    enemy_sprite.set_collision_type(ENEMY_TYPE)


    speed = random.random()*6




    movement_event = pysc.game.create_timer_trigger(20).on_reset(lambda x: enemy_sprite.move_indir(speed))
    #bullet_event = pysc.game.create_timer_trigger(150).on_reset(lambda x: create_bullet_type1((enemy_sprite.x, enemy_sprite.y), enemy_sprite.get_rotation()))
    #bullet_event = game.create_timer_trigger(1500).on_reset(lambda x: create_bullet_attracted((enemy_sprite.x, enemy_sprite.y)))

    when_hit_player = pysc.game.create_conditional_trigger(lambda: pysc.sensing.is_touching(pysc.game, enemy_sprite, pysc.game.shared_data['player']), repeats=1)
    when_leaving_screen =pysc.game.create_conditional_trigger(lambda: (enemy_sprite.y > SCREEN_HEIGHT), repeats=1)
    when_hit_by_player_bullet = pysc.game.create_type2type_collision_trigger(PLAYER_BULLET_TYPE, ENEMY_TYPE)


    


    def destroy(x):
        when_hit_player.remove()
        when_leaving_screen.remove()
        when_hit_by_player_bullet.remove()
        movement_event.remove()
        #bullet_event.remove()
        pysc.game.remove_sprite(enemy_sprite)

    def check_collision(a):
        if enemy_sprite.shape in a.shapes:
            destroy(None)

    when_hit_player.add_callback(destroy)
    when_hit_player.add_callback(lambda x: pysc.game.boardcast_message('player_health', -1))
    
    when_leaving_screen.add_callback(destroy)

    when_hit_by_player_bullet.add_callback(check_collision)

# testing only
pysc.game.create_timer_trigger(500, 20).on_reset(create_enemy_type1)