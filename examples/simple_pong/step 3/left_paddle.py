import pyscratch as pysc
game = pysc.game

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130
paddle_margin = 30

paddle = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height)
pysc.game.shared_data['left_paddle'] = paddle


def on_game_start():
    SCREEN_WIDTH = game['SCREEN_WIDTH']
    SCREEN_HEIGHT = game['SCREEN_HEIGHT']

    position = paddle_margin, SCREEN_HEIGHT//2
    paddle.set_xy(position)

    speed = 0
    while True: 
        
        if pysc.is_key_pressed('w'):
            speed -= 1
        if pysc.is_key_pressed('s'):
            speed += 1

        speed *= 0.9

        paddle.y += speed
        
        paddle.y = pysc.helper.cap(paddle.y, 0+paddle_height//2, SCREEN_HEIGHT-paddle_height//2)


        # wait for 1/60 seconds
        yield 1/60


paddle.when_game_start().add_handler(on_game_start)



