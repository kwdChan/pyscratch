import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")
# pysc.game['player'] = player  # put player as a shared variable so other sprites can access it

# Event: game start, the movement of the player
def on_game_start():
      
    player.set_rotation_style_left_right()
    speed_decay = 0.9
    speed_y = 0
    speed_x = 0

    while True:
        max_speed = 4


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

# or shorter: player.when_game_start().add_handler(on_game_start)
game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)



# Event: game start, ocean current changes
pysc.game['current_x'] = 0
pysc.game['current_y'] = 0

def ocean_current_change():
    # slowly change the current variables every 0.5 second
    while True:
        pysc.game['current_x'] += pysc.random_number(-0.1, 0.1)
        pysc.game['current_y'] += pysc.random_number(-0.1, 0.1)
        yield 0.5

pysc.game.when_game_start().add_handler(ocean_current_change)

# option 2: almost the same as above but the event will be removed when player is removed.
# player.when_game_start().add_handler(ocean_current_change)




# Event: game start, moved by the ocean current
def ocean_current_movement():
    while True:

        # you can add these two lines inside the loop in the first event as well
        # but for the code readabilty, 
        # it can be a good idea to put it out as a separate event. 
        player.x += pysc.game['current_x'] 
        player.y += pysc.game['current_y'] 
        yield 1/60

player.when_game_start().add_handler(ocean_current_movement)