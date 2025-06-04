import pyscratch as pysc
from settings import *

# TODO: bad naming consistency 
sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height,  pos=(SCREEN_WIDTH-paddle_margin, SCREEN_HEIGHT//2))

#sprite.set_draggable(True)

game_start_event = sprite.when_game_start()
def movement():
    while True: 
        speed = 0
        
        if pysc.sensing.is_key_pressed('up'):
            speed -= 8
        if pysc.sensing.is_key_pressed('down'):
            speed += 8

        sprite.y += speed
        
        sprite.y = pysc.helper.cap(sprite.y, 0+paddle_height//2, SCREEN_HEIGHT-paddle_height//2)


        # wait for 1000/60 miliseconds
        yield 1/60

game_start_event.add_callback(movement)


#def test(updown):
#    print(updown)

#sprite.when_key_pressed('space').add_callback(test)

#sprite.when_timer_above(1000).add_callback(lambda x: pysc.game.remove_sprite(sprite))

pysc.game.shared_data['right_paddle'] = sprite