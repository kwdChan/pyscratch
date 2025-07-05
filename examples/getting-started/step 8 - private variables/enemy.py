import pyscratch as pysc


# create the sprite and initial settings
enemy = pysc.create_animated_sprite("assets/other_fishes")


def enemy_on_game_start():
    enemy.set_rotation_style_left_right()
    
    # hide the parent
    enemy.hide() 
    
    # the clone appear in the same location as the parent very briefly
    # when it's created before we set it to a random location. 
    enemy.set_xy((-200, -200))  

    # clone itself very 2 seconds
    while True: 
        enemy.create_clone()
        yield 2

enemy.when_game_start().add_handler(enemy_on_game_start)


# clone movement
#def on_clone(clone_sprite): 
def on_clone(clone_sprite: pysc.Sprite): 


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
    clone_sprite['size'] = size

    # show the sprite
    clone_sprite.show()
    

    #player = pysc.game['player']
    player: pysc.Sprite = pysc.game['player']
    
    # movement
    while True:


        if player.sprite_data['size'] > size:
            clone_sprite.set_frame(1)
        else:
            clone_sprite.set_frame(0)

            
        if clone_sprite.distance_to_sprite(player) < 200:
            clone_sprite.point_towards_sprite(player)

            if player['size'] > size:
                clone_sprite.direction += 180

        

        clone_sprite.direction += pysc.random_number(-2, 2)

        clone_sprite.move_indir(2/size)
        yield 1/60

enemy.when_started_as_clone().add_handler(on_clone)


# clone touch the player 
#def clone_touch_the_player(clone_sprite):
def clone_touch_the_player(clone_sprite: pysc.Sprite):

    player: pysc.Sprite = pysc.game['player']
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()

            if player['size'] > clone_sprite['size']:
                player['size'] += 0.2
            else:
                player['size'] -= 0.2
                pysc.game['health'] -= 1
            

        yield 1/pysc.game['framerate']
    
enemy.when_started_as_clone().add_handler(clone_touch_the_player)
