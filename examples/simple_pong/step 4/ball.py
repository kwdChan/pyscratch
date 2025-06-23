import pyscratch as pysc
game = pysc.game 


# recommend a colour picking website
ball_colour = (220, 220, 220)
ball_radius = 25

ball_sprite = pysc.create_circle_sprite(ball_colour, ball_radius)


def movement():
    speed_x = 4
    speed_y = 4

    while True: 
        yield 1/60

        if game['running']:
            ball_sprite.show()

            if ball_sprite.is_touching(game['top_edge']):
                speed_y = abs(speed_y)

            if ball_sprite.is_touching(game['bottom_edge']):
                speed_y = -abs(speed_y)

            if ball_sprite.is_touching(game['left_edge']):
                speed_x = abs(speed_x)
                ball_sprite.broadcast_message('right_score')

            if ball_sprite.is_touching(game['right_edge']):
                speed_x = -abs(speed_x)
                ball_sprite.broadcast_message('left_score')

            if ball_sprite.is_touching( game['right_paddle']):
                speed_x = -abs(speed_x)
                game.play_sound('pong')

            if ball_sprite.is_touching( game['left_paddle']):
                speed_x = abs(speed_x)
                game.play_sound('pong')
                

            ball_sprite.x += speed_x
            ball_sprite.y += speed_y
        else: 
            ball_sprite.hide()
            
            ball_sprite.y = game['SCREEN_HEIGHT']//2
            ball_sprite.x = game['SCREEN_WIDTH']//2


ball_sprite.when_game_start().add_handler(movement)
