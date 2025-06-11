import pyscratch as pysc
bird = pysc.create_single_costume_sprite("examples/flappy_bird/assets/bird/20.png")
bird.set_draggable(True)

pysc.game.shared_data['speed'] = 0





# def movement():
#     speed = 0
#     while True:
#
#         # fall
#         bird.y = bird.y + speed
#
#         # falling faster and faster
#         speed = speed + 0.3
#
#         # wait for one frame
#         yield 1/60 


def movement():
    #speed = 0
    while True:
        bird.y = bird.y + pysc.game.shared_data['speed']
        pysc.game.shared_data['speed'] = pysc.game.shared_data['speed'] + 0.25
        yield 1/60

game_start_event = bird.when_game_start()
game_start_event.add_handler(movement)


def jump(updown):
    if updown == 'down':
        pysc.game.shared_data['speed'] = -7

jump_event = bird.when_key_pressed('space')
jump_event.add_handler(jump)

