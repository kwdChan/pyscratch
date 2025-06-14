import pyscratch as pysc
from settings import *

# TODO: bad naming consistency 
sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height,  position=(paddle_margin, SCREEN_HEIGHT//2))
sprite.set_draggable(True)
def movement():
    speed = 0
    while True: 
        if pysc.is_key_pressed('w'):
            speed = -8
        if pysc.is_key_pressed('s'):
            speed = 8
        
        speed *= 0.9

        sprite.y += speed
        
        sprite.y = pysc.helper.cap(sprite.y, 0+paddle_height/2, SCREEN_HEIGHT-paddle_height/2)

        yield 1/60
        
game_start_event = sprite.when_game_start()
game_start_event.add_handler(movement)







pysc.game.shared_data['left_paddle'] = sprite