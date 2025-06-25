import pyscratch as pysc


# create the sprite
enemy = pysc.create_single_costume_sprite("assets/other_fishes/0.png")

# Event: when_game_start, clone creation
def enemy_on_game_start():
    enemy.set_rotation_style_left_right()
    enemy.hide() # hide the parent

    # clone itself very 2 seconds
    while True: 
        enemy.create_clone()
        yield 2

enemy.when_game_start().add_handler(enemy_on_game_start)


# Event: when_started_as_clone, clone movement
def clone_movement(clone_sprite):

    screen_height = 720

    # start the fish from the left edge at a random height
    clone_sprite.y = pysc.random_number(0, screen_height)
    clone_sprite.x = 0

    # random size
    size = pysc.random_number(0.8, 1.2)
    clone_sprite.set_scale(size)

    # show the clone
    clone_sprite.show()

    while True:
        
        clone_sprite.move_indir(3)

        yield 1/60

enemy.when_started_as_clone().add_handler(clone_movement)
