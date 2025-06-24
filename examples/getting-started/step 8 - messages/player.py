import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")
pysc.game['player'] = player  # add the player as a shared variable so other sprites can access it

player['size'] = 1  

def on_game_start():

    player.set_rotation_style_left_right()
    speed_decay = 0.9
    speed_y = 0
    speed_x = 0

    while True:

        player.set_scale(player['size'])

        max_speed = 4/player['size']


        if pysc.is_key_pressed('w'):
            speed_y = -max_speed

        elif pysc.is_key_pressed('s'):
            speed_y = max_speed

        else:
            speed_y *= speed_decay # speed_y = speed_y * speed_decay

        if pysc.is_key_pressed('a'):
            player.direction = 180
            speed_x = -max_speed
            
        elif pysc.is_key_pressed('d'):
            player.direction = 0
            speed_x = max_speed
        else:
            speed_x *= speed_decay # speed_x = speed_y * speed_decay


        player.y += speed_y
        player.x += speed_x

        yield 1/60


game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)

# or shorter: player.when_game_start().add_handler(on_game_start)


def check_health():

    while True:
        if not pysc.game['health']:
            player.remove()
        yield 1/60


game_start_event.add_handler(check_health)



def on_size_change(change):


    each_step = change/10

    for i in range(10):
        player['size'] += each_step

        yield 0.1

player.when_receive_message('size_change').add_handler(on_size_change)
    
