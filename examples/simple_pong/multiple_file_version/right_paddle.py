
import pyscratch as pysc
from settings import *

# 2. create right paddle

right_paddle_sprite = pysc.rect_sprite(paddle_colour, paddle_width, paddle_height, pos=(SCREEN_WIDTH-paddle_margin, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(right_paddle_sprite)
right_paddle_sprite.set_collision_type(1)


## behaviour
## - move by key 'up' and 'down' in a limited space
right_timer_event = pysc.game.when_timer_reset(10)

def check_move_right(n):
    movement = 0
    if pysc.sensing.is_key_pressed('up'):
        movement -= 8

    if pysc.sensing.is_key_pressed('down'):
        movement += 8

    right_paddle_sprite.move_xy((0, movement))

    # confine the paddle within the screen
    min_y = paddle_height//2
    max_y = SCREEN_HEIGHT-paddle_height//2
    right_paddle_sprite.y = pysc.helper.cap(right_paddle_sprite.y, min_y, max_y)

right_timer_event.add_callback(check_move_right)


pysc.game.shared_data['right_paddle_sprite'] = right_paddle_sprite
