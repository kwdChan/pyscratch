import pyscratch as pysc
from settings import *

player = pysc.game.shared_data['player']

#from typing import cast
#player = cast(pysc.ScratchSprite, player)


# create the sprite and initial settings
enemy = pysc.create_single_costume_sprite("assets/fishes/18.png")
enemy.set_scale(.5)
enemy.hide()

# clone the sprite every 2 seconds
def create_enemy():
    while True: 
        enemy.clone_myself()
        yield 2

enemy.when_game_start().add_callback(create_enemy)


# clone movement
def clone_movement(clone_sprite: pysc.ScratchSprite):
    clone_sprite.show()
    clone_sprite.x = pysc.helper.random_number(0, SCREEN_WIDTH)

    if pysc.helper.random_number(0, 1) > 0.5: 
        clone_sprite.y = 0
    else:
        clone_sprite.y = SCREEN_HEIGHT


    while True:
        clone_sprite.point_towards_sprite(player)
        clone_sprite.move_indir(1)
        yield 1/FRAMERATE

enemy.when_started_as_clone().add_callback(clone_movement)

# clone touch the player 
def clone_touch_the_player(clone_sprite: pysc.ScratchSprite):
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()
            player.scale_by(0.7)
            pysc.game.shared_data['health'] -= 1
            

        yield 1/FRAMERATE
    
enemy.when_started_as_clone().add_callback(clone_touch_the_player)
