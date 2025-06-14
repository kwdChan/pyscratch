import pyscratch as pysc
from settings import *

player = pysc.game.shared_data['player']

#from typing import cast
#player = cast(pysc.ScratchSprite, player)


# create the sprite and initial settings
#enemy = pysc.create_single_costume_sprite("assets/fishes/18.png")
enemy = pysc.create_animated_sprite("assets/kenney/other_fishes")
enemy.set_rotation_style_left_right()
enemy.hide()

# clone the sprite every 2 seconds
def create_enemy():
    while True: 
        enemy.clone_myself()
        yield 2

enemy.when_game_start().add_handler(create_enemy)


# clone movement
def clone_movement(clone_sprite: pysc.Sprite):
    clone_sprite.show()

    # random height
    clone_sprite.y = pysc.helper.random_number(0, SCREEN_HEIGHT)

    # randomly either from the left or from the right
    if pysc.helper.random_number(0, 1) > 0.5: 
        clone_sprite.x = 0
        clone_sprite.direction = 0 # left to right
    else:
        clone_sprite.x = SCREEN_WIDTH
        clone_sprite.direction = 180 # right to left


    # random size
    size = pysc.helper.random_number(0.3, 2)
    clone_sprite.set_scale(size)

    clone_sprite.private_data['size'] = size

    while True:
        if player.private_data['size'] > size:
            clone_sprite.set_frame(1)
        else:
            clone_sprite.set_frame(0)

            
        if clone_sprite.distance_to_sprite(player) < (100+player.private_data['size']*100):
            clone_sprite.point_towards_sprite(player)

            if player.private_data['size'] > size:
                clone_sprite.direction += 180



        clone_sprite.direction += pysc.helper.random_number(-2, 2)

        clone_sprite.move_indir(2/size)
        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(clone_movement)

# clone touch the player 
def clone_touch_the_player(clone_sprite: pysc.Sprite):
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()

            if player.private_data['size'] > clone_sprite.private_data['size']:
                player.private_data['size'] += 0.2
            else:
                player.private_data['size'] -= 0.2
                pysc.game.shared_data['health'] -= 1
            

        yield 1/FRAMERATE
    
enemy.when_started_as_clone().add_handler(clone_touch_the_player)
