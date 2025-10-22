import pyscratch as pysc
from pyscratch import game

friend = pysc.create_single_costume_sprite("assets/fish_orange_outline.png")

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
        


def check_if_centred():
    """
    when_game_start: 
    move away when near the centre
    """
    centre = game.screen_width/2, game.screen_height/2
    while True:
        yield 1/game.framerate
        if friend.distance_to(centre) < 50:
            game['score'] += 10

            new_x = pysc.random_number(0, game.screen_width)
            new_y = pysc.random_number(0, game.screen_height)

            friend.x = new_x
            friend.y = new_y
    
friend.when_game_start().add_handler(check_if_centred)
        

def when_clicked():
    """
    flash the friend when clicked
    """
    for i in range(5):
        friend.hide()
        yield 0.1
        friend.show()
        yield 0.1

friend.when_this_sprite_clicked().add_handler(when_clicked)


def lose():
    """
    hide when lose
    """
    friend.hide()

friend.when_backdrop_switched("lose").add_handler(lose)