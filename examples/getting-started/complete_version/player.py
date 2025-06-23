import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/kenney/player.png")

# variable definitons should be done outside the event to guarantee the variables is defined before any event try to access it 
player['size'] = 1  


# def movement():
#     player.set_rotation_style_left_right()
#     while True:
#         if pysc.sensing.is_key_pressed('w'):
#             player.y -= 4

#         if pysc.sensing.is_key_pressed('s'):
#             player.y += 4

#         if pysc.sensing.is_key_pressed('a'):
#             player.direction = 180
#             player.x -= 4
            
#         if pysc.sensing.is_key_pressed('d'):
#             player.direction = 0
#             player.x += 4

#         yield 1/FRAMERATE


def movement():
    player.set_draggable(True)
      
    player.set_rotation_style_left_right()
    speed_decay = 0.9
    speed_y = 0
    speed_x = 0

    while True:


        player.point_towards_mouse()
        player.move_indir(4)
        yield 1/pysc.game['framerate']
        continue
        player.set_scale(player['size'])
        max_speed = 4


        if pysc.is_key_pressed('w'):
            speed_y = -max_speed

        elif pysc.is_key_pressed('s'):
            speed_y = max_speed

        else:
            speed_y *= speed_decay

        if pysc.is_key_pressed('a'):
            player.direction = 180
            speed_x = -max_speed
            
        elif pysc.is_key_pressed('d'):
            player.direction = 0
            speed_x = max_speed
        else:
            speed_x *= speed_decay


        player.y += speed_y
        player.x += speed_x

        yield 1/pysc.game['framerate']


game_start_event = player.when_game_start()
game_start_event.add_handler(movement)



def check_health():

    while True:
        if not pysc.game['health']:
            player.remove()
        yield 1/60


game_start_event.add_handler(check_health)

pysc.game['player'] = player

