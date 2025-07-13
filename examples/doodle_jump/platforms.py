import pyscratch as pysc
from pyscratch import game

def Platform(position):
    sp = pysc.create_animated_sprite("assets/used_by_examples/doodle_jump/platform")
    sp.x = position[0]
    sp['world_y'] = position[1]
    game.move_to_back(sp)

    sp.y = sp['world_y'] -game['view_y']
    player = game['player']
    def movement_and_touch(_):
        while True:
            yield 1/game.framerate
            sp.y = sp['world_y'] -game['view_y']
            if sp.is_touching(player) and (player['vy']>0):
                game.broadcast_message('jump')

    sp.when_timer_above(0).add_handler(movement_and_touch)
    return sp

game.when_game_start().add_handler(lambda: Platform((300, 1000)))
game.when_game_start().add_handler(lambda: Platform((300, 800)))


def create_platform():

    platforms = []
    for i in range(20):
        y = i*pysc.random_number(70, 100)
        p = Platform((pysc.random_number(0, game.screen_width), y))
        platforms.append(p)

    while True:
        yield 1/game.framerate
        platforms = [p for p in platforms if p.y<0]
        if len(platforms) < 5:
            #print(len(platforms))

            y = 3*pysc.random_number(70, 100)
            p = Platform((pysc.random_number(0, game.screen_width), game['view_y']-y))
            print(p.y)
            platforms.append(p)

    



    

game.when_game_start().add_handler(create_platform)