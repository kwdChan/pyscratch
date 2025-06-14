import pyscratch as pysc
from settings import * 

score_board = pysc.create_rect_sprite((200, 200, 200), 150, 70, position=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
game_start_event = score_board.when_game_start()
pysc.game.shared_data['left_score'] = 0
pysc.game.shared_data['right_score'] = 0

def display_score():
    pysc.game.show_sprite(score_board)
    l = pysc.game.shared_data['left_score'] 
    r = pysc.game.shared_data['right_score'] 
    score_board.write_text(f'{l} - {r}', font, offset=(150//2, 70//2))

game_start_event.add_handler(display_score)


left_score_event = score_board.when_receive_message('left_score')
def left_score(data):
    pysc.game.shared_data['left_score'] += 1 
    pysc.game.shared_data['running'] = False

    display_score()

left_score_event.add_handler(left_score)


right_score_event = score_board.when_receive_message('right_score')
def right_score(data):
    pysc.game.shared_data['right_score'] += 1 
    pysc.game.shared_data['running'] = False

    display_score()

right_score_event.add_handler(right_score)

on_click = score_board.when_this_sprite_clicked()
resume_game_event = pysc.game.when_any_key_pressed()

def resume_game():
    pysc.game.shared_data['running'] = True
    pysc.game.hide_sprite(score_board)

def on_space_release(key, updown):
    if key == 'space' and updown == 'up':
        resume_game()


resume_game_event.add_handler(on_space_release)
on_click.add_handler(resume_game)


