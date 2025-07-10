import pyscratch as pysc
from pyscratch import game

player = pysc.create_single_costume_sprite("assets/used_by_examples/bullet_hell/player.png")
game['player'] = player
def movement():
    player.set_scale(3)
    player.set_xy((360, 1080))
    

    speed = 8

    while True:
        yield 1/game.framerate

        if pysc.is_key_pressed('w'):
            player.y -= speed

        if pysc.is_key_pressed('s'):
            player.y += speed

        if pysc.is_key_pressed('a'):
            player.x -= speed     

        if pysc.is_key_pressed('d'):
            player.x += speed

player.when_game_start().add_handler(movement)


def shoot_bullet():
    Bullet = game['Bullet']
    bullet_speed = 10
    while True: 
        yield 0.8

        Bullet(player.x, player.y-35, bullet_speed)

player.when_game_start().add_handler(shoot_bullet)