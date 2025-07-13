from numpy import True_
import pyscratch as pysc
from pyscratch import game

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

# TODO: recommend a colour picking website
ball_colour = (220, 220, 220)
ball_radius = 25
ball_sprite = pysc.create_circle_sprite(ball_colour, ball_radius, position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
game['ball_sprite'] = ball_sprite

top_edge, left_edge, bottom_edge, right_edge = pysc.create_edge_sprites(thickness=0)

 
def movement():
    speed_x = 3
    speed_y = 3
    pong = False

    while True: 
        yield .5/game.framerate # wait for half a frame (for smoothness)
        

        if game['running']:
            
            ball_sprite.show()
            if ball_sprite.is_touching(top_edge):
                pong = True
                speed_y = abs(speed_y)

            elif ball_sprite.is_touching(bottom_edge):
                pong = True
                speed_y = -abs(speed_y)

            elif ball_sprite.is_touching(left_edge):
                speed_x = abs(speed_x)
                ball_sprite.broadcast_message('right_score')
                game['running'] = False
                pong = False

            elif ball_sprite.is_touching(right_edge):
                speed_x = -abs(speed_x)
                ball_sprite.broadcast_message('left_score')
                game['running'] = False
                pong = False

            elif ball_sprite.is_touching(game['right_paddle']):
                pong = True
                speed_x = -abs(speed_x)

            elif ball_sprite.is_touching(game['left_paddle']):
                pong = True
                speed_x = abs(speed_x)

            elif pong:
                game.play_sound('pong')
                pong = False

                
            ball_sprite.x += speed_x
            ball_sprite.y += speed_y
        else:
            ball_sprite.hide()
            
            ball_sprite.y = SCREEN_HEIGHT//2
            ball_sprite.x = SCREEN_WIDTH//2
    
game_start_event = ball_sprite.when_game_start()
game_start_event.add_handler(movement)

