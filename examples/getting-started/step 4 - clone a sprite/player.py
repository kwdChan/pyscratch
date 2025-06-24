import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")

# free to use any function name
def on_game_start():

    player.set_rotation_style_left_right()
    while True:
        if pysc.is_key_pressed('w'):
            player.y -= 4

        if pysc.is_key_pressed('s'):
            player.y += 4

        if pysc.is_key_pressed('a'):
            player.direction = 180
            player.x -= 4
            
        if pysc.is_key_pressed('d'):
            player.direction = 0
            player.x += 4

        yield 1/60 # because the frame rate is 60


game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)

# or shorter: player.when_game_start().add_handler(on_game_start)

