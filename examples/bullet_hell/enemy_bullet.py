import pyscratch as pysc
from pyscratch import game


def StandardBullet(position, direction, speed):

    bullet = pysc.create_animated_sprite(
        "assets/used_by_examples/bullet_hell/normal_bullet",
        position=position)
    
    bullet.direction = direction
    bullet.set_scale(1.5)

    
    bullet['movement_event'] = movement_event = bullet.when_timer_reset(1/game.framerate).add_handler(lambda _: bullet.move_indir(speed))
    bullet.when_timer_reset(0.2).add_handler(lambda _: bullet.next_frame())
    
    def detect_collision(_):
        player = game['player']

        if bullet.is_touching(player):
            movement_event.remove()
            bullet.when_timer_reset(0.1, 1).add_handler(lambda _: bullet.remove())

    bullet.when_timer_reset(1/game.framerate).add_handler(detect_collision)
    return bullet
        
game['StandardBullet'] = StandardBullet



def ExplodingBullet(position, direction, lifespan):
    speed = 5
    main_bullet = StandardBullet(position, direction, speed)

    def explode():
        main_bullet['movement_event'].remove()
        main_bullet.remove()
        for i in range(12):
            StandardBullet((main_bullet.x, main_bullet.y), i*30, speed*1.5)

    
    main_bullet.when_timer_reset(lifespan, 1).add_handler(lambda _: explode())


game['ExplodingBullet'] = ExplodingBullet

