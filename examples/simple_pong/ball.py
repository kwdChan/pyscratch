import pyscratch as pysc
from settings import * 


# recommend a colour picking website
ball_colour = (220, 220, 220)
ball_radius = 25

ball_sprite = pysc.create_circle_sprite(ball_colour, ball_radius, pos = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))


game_start_event = ball_sprite.when_game_start()


def movement():
    speed_x = 4
    speed_y = 4

    while True: 
        yield 1/60
        if pysc.game.shared_data['running']:
            pysc.game.show_sprite(ball_sprite)
            if pysc.sensing.is_touching(ball_sprite, top_edge):
                speed_y = abs(speed_y)

            if pysc.sensing.is_touching( ball_sprite, bottom_edge):
                speed_y = -abs(speed_y)

            if pysc.sensing.is_touching(ball_sprite, left_edge):
                speed_x = abs(speed_x)
                ball_sprite.broadcast_message('right_score', None)

            if pysc.sensing.is_touching( ball_sprite, right_edge):
                speed_x = -abs(speed_x)
                ball_sprite.broadcast_message('left_score', None)

            if pysc.sensing.is_touching( ball_sprite, pysc.game.shared_data['right_paddle']):
                speed_x = -abs(speed_x)
                pysc.game.play_sound('bong')

            if pysc.sensing.is_touching( ball_sprite, pysc.game.shared_data['left_paddle']):
                speed_x = abs(speed_x)
                pysc.game.play_sound('bong')
                
            ball_sprite.x += speed_x
            ball_sprite.y += speed_y
        else:
            # TODO: make into a method of the sprite
            pysc.game.hide_sprite(ball_sprite)
            
            ball_sprite.y = SCREEN_HEIGHT//2
            ball_sprite.x = SCREEN_WIDTH//2

        

    

game_start_event.add_callback(movement)

pysc.game.shared_data['ball_sprite'] = ball_sprite
