import pyscratch as pysc
from pyscratch import game

def FishSprite():
    sp = pysc.create_animated_sprite("assets/some_fishes")

    def point_to_mouse():

        sp.x = pysc.random_number(0, game.screen_width)
        sp.y = pysc.random_number(0, game.screen_height)

        while True: 
            yield 1/game.framerate
            sp.point_towards_mouse()
            sp.move_indir(5)
        
    sp.when_game_start().add_handler(point_to_mouse)

    return sp

n_fish = 20
fishes = []
for i in range(n_fish):
    fishes.append(FishSprite())



from typing import List
import numpy as np

def get_dist(me: pysc.Sprite, others: List[pysc.Sprite]):

    distances = [me.distance_to_sprite(another) if not  me is another else np.inf for another in others ]
    ind = np.argsort(distances)#[::-1]

    ideal_dist = 200
    max_speed = 5

    div = ideal_dist/max_speed
    for n in ind[:n_fish-1]:
        n_nearest_other = others[n]

        if me.x > n_nearest_other.x:
            me.x += (ideal_dist - (me.x - n_nearest_other.x))/div

        elif me.x < n_nearest_other.x:
            me.x -= (ideal_dist - (n_nearest_other.x - me.x))/div

        if me.y > n_nearest_other.y:
            me.y += (ideal_dist - (me.y - n_nearest_other.y))/div

        elif me.y < n_nearest_other.y:
            me.y -= (ideal_dist - (n_nearest_other.y - me.y))/div


def keep_distance(_):
    for f in fishes:
        f.x = pysc.random_number(0, pysc.game.screen_width)
        f.y = pysc.random_number(0, pysc.game.screen_height)

    while True:
        yield 1/pysc.game.framerate
        for f in fishes:
            get_dist(f, fishes)

temp_e = pysc.game.when_timer_above(0)
temp_e.add_handler(keep_distance)