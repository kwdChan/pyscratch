import pyscratch as pysc
from pyscratch import game

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130
paddle_margin = 30

sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height,  position=(SCREEN_WIDTH-paddle_margin, SCREEN_HEIGHT//2))

#sprite.set_draggable(True)

game_start_event = sprite.when_game_start()
def movement():
    while True: 
        speed = 0
        
        if pysc.is_key_pressed('up'):
            speed -= 8
        if pysc.is_key_pressed('down'):
            speed += 8

        sprite.y += speed
        
        sprite.y = pysc.cap(sprite.y, 0+paddle_height//2, SCREEN_HEIGHT-paddle_height//2)


        # wait for 1 frame
        yield 1/game.framerate

game_start_event.add_handler(movement)


game['right_paddle'] = sprite