
import pyscratch as pysc
from settings import *

# 1. create left paddle
left_paddle_sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height, pos=(paddle_margin, SCREEN_HEIGHT//2))
#pysc.game.add_sprite(left_paddle_sprite)
left_paddle_sprite.set_collision_type(1) # enables the collision


## behaviour
## - move by key 'a' and 'd' in a limited space

left_timer_event = pysc.game.when_timer_reset(10) # run every 10ms, repeats=np.inf by default

def check_move_left(n): # the parameter n is the number of repeats left in the trigger. unused in this case.
    movement = 0
    if pysc.sensing.is_key_pressed('w'):
        movement -= 8

    if pysc.sensing.is_key_pressed('s'):
        movement += 8

    left_paddle_sprite.move_xy((0, movement))

    # confine the paddle within the screen
    min_y = paddle_height//2
    max_y = SCREEN_HEIGHT-paddle_height//2
    left_paddle_sprite.y = pysc.helper.cap(left_paddle_sprite.y, min_y, max_y)

left_timer_event.add_callback(check_move_left)

## use pysc.game.shared_data instead of import 
# 1. to avoid circular import
# 2. minimise the number of imports for the ease of opening a new file
pysc.game.shared_data['left_paddle_sprite'] = left_paddle_sprite
