import pyscratch as pysc


# create the sprite and initial settings
#enemy = pysc.create_animated_sprite("assets/other_fishes")
enemy = pysc.create_single_costume_sprite("assets/other_fishes/0.png")


def enemy_on_game_start():
    enemy.set_rotation_style_left_right()

    # hide the parent
    enemy.hide() 

    # clone itself very 2 seconds
    while True: 
        enemy.create_clone()
        yield 2

enemy.when_game_start().add_handler(enemy_on_game_start)


# clone movement
#def on_clone(clone_sprite): 
def on_clone(clone_sprite: pysc.Sprite): 

    #clone_sprite.hide()
    # random height
    clone_sprite.y = pysc.random_number(0, 720)

    # randomly either from the left or from the right
    if pysc.random_number(0, 1) > 0.5: 
        clone_sprite.x = 0
        clone_sprite.direction = 0 # left to right
    else:
        clone_sprite.x = 1280
        clone_sprite.direction = 180 # right to left

    # random size
    size = pysc.random_number(0.3, 2)
    clone_sprite.set_scale(size)

    # show the sprite
    clone_sprite.show()
    

    #player = pysc.game['player']
    player: pysc.Sprite = pysc.game['player']
    
    # movement
    while True:

        if clone_sprite.distance_to_sprite(player) < 200:
            clone_sprite.point_towards_sprite(player)    

        clone_sprite.direction += pysc.random_number(-2, 2)

        clone_sprite.move_indir(2)
        yield 1/60

enemy.when_started_as_clone().add_handler(on_clone)


# clone touch the player 
#def clone_touch_the_player(clone_sprite):
def clone_touch_the_player(clone_sprite: pysc.Sprite):

    player: pysc.Sprite = pysc.game['player']
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()

            pysc.game['health'] -= 1
            

        yield 1/pysc.game['framerate']
    
enemy.when_started_as_clone().add_handler(clone_touch_the_player)
