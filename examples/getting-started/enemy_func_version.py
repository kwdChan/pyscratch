import pyscratch as pysc
from settings import *

player = pysc.game.shared_data['player']

#from typing import cast
#from pyscratch.scratch_sprite import ScratchSprite
#player = cast(ScratchSprite, player)

def create_enemy(_):
    enemy = pysc.create_animated_sprite("assets/kenney/other_fishes")
    enemy.set_rotation_style_left_right()

    enemy.set_scale(.5)
    enemy.x = pysc.helper.random_number(0, SCREEN_WIDTH)


    if pysc.helper.random_number(0, 1) > 0.5: 
        enemy.y = 0
    else:
        enemy.y = SCREEN_HEIGHT

    def movement(_):
        while True:
            enemy.point_towards_sprite(player)
            enemy.move_indir(1)
            yield 1/FRAMERATE
    enemy.when_timer_above(0).add_handler(movement)


pysc.game.when_timer_reset(2).add_handler(create_enemy)