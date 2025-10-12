import pyscratch as pysc
game = pysc.game

enemy = pysc.create_single_costume_sprite("assets/fish_red_skeleton_outline.png")
#enemy.set_draggable(True)


def clicked():
    """
    when the enemy is clicked: 
    change the enemy location with a fade out effect
    """
    for i in range(10):
        yield 1/game.framerate
        enemy.set_transparency(1-i/10) # print(1-i/10) if you find this confusing.
        enemy.scale_by(0.9)

    enemy.x = pysc.random_number(0, game.screen_width)
    enemy.y = pysc.random_number(0, game.screen_height)

    enemy.set_transparency(1)
    enemy.set_scale(1)
    
enemy.when_this_sprite_clicked().add_handler(clicked)


def movement():
    """
    when_game_start: 
    the movement of the enemy
    """

    speed = 5
    centre = (game.screen_width/2, game.screen_height/2)

    while True:
        yield 1/game.framerate

        # get the distance to the mouse
        mouse_x, mouse_y = pysc.get_mouse_pos()
        distance_to_mouse = enemy.distance_to((mouse_x, mouse_y))

        # enemy avoids the mouse when it is close to the mouse
        if distance_to_mouse < 200:
            enemy.point_towards_mouse()
            enemy.direction += 180
            enemy.move_indir(speed)
        
        # otherwise, go to the centre of the screen 
        else:
            enemy.point_towards(centre)
            enemy.move_indir(speed)


enemy.when_game_start().add_handler(movement)
        