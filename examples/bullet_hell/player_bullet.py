import pyscratch as pysc
from pyscratch import game

game['player_bullets'] = []
def Bullet(x, y, speed):
    bullet = pysc.create_single_costume_sprite(
        "assets/used_by_examples/bullet_hell/orb_bullets/6.png",
        position=(x,y)
    )
    bullet.x = x
    bullet.y = y
    bullet.set_scale(0.5)

    def movement(_):
        while True:
            yield 1/game.framerate
            bullet.y -= speed

    bullet.when_timer_above(0).add_handler(movement)


    game['player_bullets'].append(bullet)
    #return bullet

game['Bullet'] = Bullet


def clear_removed_bullet(_):
    game['player_bullets'] = [b for b in game['player_bullets'] if not b.removed]

game.when_timer_reset(2).add_handler(clear_removed_bullet)