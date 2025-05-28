import pyscratch as pysc
from setting import *
import random 

def shoot_player_bullet(player):

    bullet = pysc.ScratchSprite(frames, "circle_bullets", player.body.position)

    pysc.game.add_sprite(bullet)
    bullet.set_collision_type(PLAYER_BULLET_TYPE)
    bullet.set_rotation(-90)

    movement_timer = pysc.game.create_timer_trigger(1000/240).on_reset(
        lambda x: bullet.move_indir(2)
    )

    next_frame_timer = pysc.game.create_timer_trigger(100).on_reset(
        lambda x: bullet.next_frame()
    )


    def destroy_when_exit(x):
        movement_timer.remove()
        next_frame_timer.remove()
        pysc.game.remove_sprite(bullet)


    destroy_condition = pysc.game.create_conditional_trigger(lambda: (bullet.y < 0), repeats=1)
    destroy_condition.add_callback(destroy_when_exit)




pysc.game.create_messager_trigger('player_shoot_bullet').add_callback(shoot_player_bullet)
