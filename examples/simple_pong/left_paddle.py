import pyscratch as pysc
from pyscratch import game

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130
paddle_margin = 30


sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height,  position=(paddle_margin, SCREEN_HEIGHT//2))
game['left_paddle'] = sprite
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
        
        sprite.y = pysc.cap(sprite.y, 0+paddle_height/2, SCREEN_HEIGHT-paddle_height/2)

        yield 1/game.framerate
        
game_start_event = sprite.when_game_start()
game_start_event.add_handler(movement)


