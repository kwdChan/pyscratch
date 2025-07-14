import numpy as np
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


def Laser(pos0, pos1, duration):

    len_x = pos1[0]-pos0[0]
    len_y = pos1[1]-pos0[1]

    length = (len_x**2 + len_y**2)**(1/2)

    
    path = "assets/used_by_examples/bullet_hell/lasers/3.png"
    img = pysc.load_image(path)
    w = img.get_width()

    scaled_img = pysc.scale_to_fill(img, (w, length))



    laser_sp = pysc.Sprite(dict(always=[scaled_img]))

    laser_sp.direction = -np.arctan(len_x/len_y)/np.pi*180
    laser_sp.x = (pos1[0]+pos0[0])/2
    laser_sp.y = (pos1[1]+pos0[1])/2
    laser_sp.set_transparency(0)
    def change_alpha(_):
        for i in range(30):
            laser_sp.set_transparency(i/30)
            yield 0.01
        for i in range(30):
            laser_sp.set_transparency(1-i/30)
            yield 0.01            
        laser_sp.remove()
    laser_sp.when_timer_above(0).add_handler(change_alpha)


game['Laser'] = Laser


    
    

