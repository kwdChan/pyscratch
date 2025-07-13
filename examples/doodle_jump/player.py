from shutil import move
import pyscratch as pysc
from pyscratch import game
from pyscratch.game_module import is_key_pressed

player_skin = pysc.create_animated_sprite("assets/used_by_examples/doodle_jump/player")
player = pysc.create_rect_sprite((0,0,0), 70, 20, position=(370, 900))
player.set_transparency(0)


game['player'] = player
game['gravity'] = 500
player['vy'] = 0
player['world_y'] = 900
game['view_y'] = 0

def movement():
    x_speed = 300
    dt = 1/game.framerate
    player_skin.set_rotation_style_left_right()
    #game.bring_to_front(player_skin)
    while True:
        player_skin.x = player.x
        player_skin.y = player.y-60
        yield dt

        player['vy'] += game['gravity']*dt
        player['world_y'] += player['vy']*dt
        player.y = player['world_y']-game['view_y']

        game['view_y'] = min(player['world_y']-900, game['view_y'])

        if pysc.is_key_pressed('left'):
            player.x -= x_speed*dt
            player_skin.direction=0

        if pysc.is_key_pressed('right'):
            player.x += x_speed*dt
            player_skin.direction=180


player.when_game_start().add_handler(movement)


def on_msg_jump(_):
    player['vy'] = -500
    player_skin.set_frame(1)
    yield 0.3
    player_skin.set_frame(0)


player.when_receive_message('jump').add_handler(on_msg_jump)
