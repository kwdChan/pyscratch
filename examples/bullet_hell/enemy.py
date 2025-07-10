import pyscratch as pysc
from pyscratch import game

def Enemy(position, speed, frame_idx, direction, bullet_period=0.4, path="assets/used_by_examples/bullet_hell/enemy"):
    enemy = pysc.create_animated_sprite(
        path,
        position=position
        )
    enemy.set_animation('normal')
    enemy.direction = direction#-90
    enemy.set_frame(frame_idx)
    enemy.set_scale(6/speed)


    def movement(_):
        while True: 
            yield 1/game.framerate

            enemy.move_indir(speed, 90)

    movement_event = enemy.when_timer_above(0).add_handler(movement)

    
    def explode_and_remove():
        movement_event.remove()
        enemy.set_animation('explosion')
        enemy.direction=0
        enemy.scale_by(1.3)
        enemy.when_timer_reset(0.1, 11).add_handler(lambda _: enemy.next_frame())
        enemy.when_timer_reset(0.1*11, 1).add_handler(lambda _: enemy.remove())

    def touch_player_bullet(_):
        player = game['player']

        while True: 
            yield 1/game.framerate
            if enemy.is_touching(player):
                explode_and_remove()
                return

            for b in game['player_bullets']:
                if enemy.is_touching(b):
                    b.remove()
                    explode_and_remove()
            
                    return

    enemy.when_timer_above(0).add_handler(touch_player_bullet)

    # shoot bullets
    StandardBullet = game['StandardBullet']
    enemy.when_timer_reset(bullet_period).add_handler(lambda _:  StandardBullet((enemy.x, enemy.y), direction+90, 10))

    return enemy


def spawn_standard_enemy():

    x = pysc.random_number(0, game.screen_width)
    y = 0
    frame_idx = int(pysc.random_number(0, 9.999))

    direction = pysc.random_number(-10, 10)

    Enemy((x,y), pysc.random_number(2, 6), frame_idx, direction)

def spawn_line():
    n = 6
    margin = 20
    itv = (game.screen_width-margin*2)//(n-1)
    y=0
    for i in range(n):

        x = itv*i+margin

        Enemy((x, y), 5, 0, 0, bullet_period=1)
    

def spawn_6_side_entry():

    pos1 = (0, 200)
    pos2 = (0, 400)
    pos3 = (0, 600)

    pos4 = (game.screen_width, 200)
    pos5 = (game.screen_width, 400)
    pos6 = (game.screen_width, 600)

    speed = 5
    fidx = 2

    Enemy(pos1, speed, fidx, 45-90)
    Enemy(pos2, speed, fidx, 45-90)
    Enemy(pos3, speed, fidx, 45-90)


    Enemy(pos4, speed, fidx, 45)
    Enemy(pos5, speed, fidx, 45)
    Enemy(pos6, speed, fidx, 45)


    

def spawn_kamikaze():
    x = pysc.random_number(0, game.screen_width)
    y = 0
    frame_idx = int(pysc.random_number(0, 9.999))
    direction = pysc.random_number(-10, 10)

    e = Enemy((x,y), 5, frame_idx, direction, bullet_period=1000)

    # move towards player
    e.when_timer_reset(1/game.framerate, int(10*game.framerate)).add_handler(lambda _: e.point_towards_sprite(game['player'], -90))

def spawn_laser_enemy(x, y):

    e = Enemy((x,y), speed=1, frame_idx=0, direction=0, bullet_period=1000, path="assets/used_by_examples/bullet_hell/enemy")
    e.set_animation('laser')
    e.scale_by(0.7)

    Laser = game['Laser']
    #player = game['player']
    e.when_timer_reset(3).add_handler(lambda _: Laser((e.x, e.y), (e.x, e.y+1000), 1))

def spawn_laser_enemy_pair(x):
    spawn_laser_enemy(x, 0)
    spawn_laser_enemy(game.screen_width-x, 0)



game.when_timer_reset(2).add_handler(lambda _:spawn_standard_enemy()) 

game.when_timer_above(3).add_handler(lambda _: spawn_line())
game.when_timer_above(4).add_handler(lambda _: spawn_6_side_entry())

game.when_timer_reset(7).add_handler(lambda _: spawn_line())
game.when_timer_reset(6).add_handler(lambda _: spawn_6_side_entry())

game.when_timer_reset(3).add_handler(lambda _: spawn_kamikaze())

game.when_timer_reset(5).add_handler(lambda _: game['ExplodingBullet']((720/2-pysc.random_number(-50, 50), 0), 90, 5))

game.when_timer_reset(10).add_handler(lambda _: spawn_laser_enemy(pysc.random_number(0, game.screen_width), 0))


#game.when_timer_reset(1).add_handler(lambda _: game['Laser']((0, 0), (game['player'].x, game['player'].y), 1))




        

