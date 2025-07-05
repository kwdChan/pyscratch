import pyscratch as pysc
from pyscratch.game_module import is_key_pressed


# my_sprite = pysc.create_animated_sprite("assets/run")

# def animate():
#     my_sprite.scale_by(5)
#     while True:
#         yield 0.2
#         my_sprite.next_frame()

# my_sprite.when_game_start().add_handler(animate)


my_sprite = pysc.create_animated_sprite("assets/my_sprite")
my_sprite.oob_limit=100

# variables for this sprite only
my_sprite['frame_interval'] = 0.4

# Event: on game start: switch frame
def animate():
    my_sprite.set_draggable(True)
    my_sprite.direction = 20
    my_sprite.scale_by(5)
    my_sprite.set_animation("idle") # reference the folder name of the animation
    while True:
        yield my_sprite['frame_interval']
        my_sprite.next_frame()

my_sprite.when_game_start().add_handler(animate)
#pysc.game._left_edge.hide()

# Event: on game start: movement
def movement(): 
    speed = 10
    
    #my_sprite.set_rotation_style_left_right()
    while True:
        yield 1/30
        my_sprite.if_on_edge_bounce()

        if pysc.is_key_pressed("d"):
            my_sprite.set_animation("run")
            #my_sprite.direction = 0
            my_sprite.x += speed
            my_sprite['frame_interval'] = 0.2

        elif pysc.is_key_pressed("a"):
            my_sprite.set_animation("run")
            #my_sprite.direction = 180
            my_sprite.x -= speed
            my_sprite['frame_interval'] = 0.2

        elif pysc.is_key_pressed("s"):
            my_sprite.set_animation("run")
            #my_sprite.direction = 180
            my_sprite.y += speed
            my_sprite['frame_interval'] = 0.2

        elif pysc.is_key_pressed("w"):
            my_sprite.set_animation("run")
            #my_sprite.direction = 180
            my_sprite.y -= speed
            my_sprite['frame_interval'] = 0.2

        elif pysc.is_key_pressed("space"):
            my_sprite.set_animation("run")
            #my_sprite.direction = 180
            my_sprite.move_indir(speed, -180)
            my_sprite['frame_interval'] = 0.2
        else: 
            my_sprite.set_animation("idle")
            my_sprite['frame_interval'] = 0.4

my_sprite.when_game_start().add_handler(movement)


