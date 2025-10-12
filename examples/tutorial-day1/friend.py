import pyscratch as pysc
import pygame
game = pysc.game

friend = pysc.create_single_costume_sprite("assets/fish_orange_outline.png")

# 3. Flow
def movement():
    """
    when_game_start: 
    the movement of the friend: always moving away from the curosr
    """
    centre = game.screen_width/2, game.screen_height/2
    while True:
        yield 1/game.framerate
        mouse_x, mouse_y = pysc.get_mouse_pos()
        if friend.distance_to((mouse_x, mouse_y)) < 200:
            friend.point_towards_mouse()
            friend.direction += 180
            friend.move_indir(2)
        
        else:
            friend.point_towards(centre)
            friend.move_indir(2)

friend.when_game_start().add_handler(movement)
        


# 3. Flow
# 4. Variable
def check_if_centred():
    """
    when_game_start: 
    move away when near the centre
    """
    centre = game.screen_width/2, game.screen_height/2
    while True:
        yield 1/game.framerate
        if friend.distance_to(centre) < 50:
            new_x = pysc.random_number(0, game.screen_width)
            new_y = pysc.random_number(0, game.screen_height)

            friend.x = new_x
            friend.y = new_y
            game['score'] += 10
    
friend.when_game_start().add_handler(check_if_centred)
        


