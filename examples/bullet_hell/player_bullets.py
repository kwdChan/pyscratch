import pyscratch as pysc
from setting import *
import random 

def shoot_player_bullet(player):

    bullet = pysc.Sprite(frames, "circle_bullets", player.body.position)

    #pysc.game.add_sprite(bullet)
    bullet.set_collision_type(PLAYER_BULLET_TYPE)
    bullet.set_rotation(-90)

    movement_timer = pysc.game.when_timer_reset(1000/240).add_handler(
        lambda x: bullet.move_indir(2)
    )

    next_frame_timer = pysc.game.when_timer_reset(100).add_handler(
        lambda x: bullet.next_frame()
    )


    def destroy_when_exit(x):
        movement_timer.remove()
        next_frame_timer.remove()
        pysc.game.remove_sprite(bullet)


    destroy_condition = pysc.game.when_condition_met(lambda: (bullet.y < 0), repeats=1)
    destroy_condition.add_handler(destroy_when_exit)




pysc.game.when_receive_message('player_shoot_bullet').add_handler(shoot_player_bullet)
