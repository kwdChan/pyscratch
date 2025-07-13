from attr import s
import pyscratch as pysc
import pygame
from pyscratch import game

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

font = pygame.font.SysFont(None, 48)


score_board = pysc.create_rect_sprite((200, 200, 200), 150, 70, position=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
game_start_event = score_board.when_game_start()
game['left_score'] = 0
game['right_score'] = 0

def display_score():
    score_board.show()
    l = game['left_score'] 
    r = game['right_score'] 
    score_board.write_text(f'{l} - {r}', font, offset=(150//2, 70//2))

game_start_event.add_handler(display_score)


left_score_event = score_board.when_receive_message('left_score')
def left_score(data):
    game['left_score'] += 1 
    display_score()

left_score_event.add_handler(left_score)


right_score_event = score_board.when_receive_message('right_score')
def right_score(data):
    game['right_score'] += 1 
    display_score()

right_score_event.add_handler(right_score)


def resume_game():
    game['running'] = True
    score_board.hide()

def on_space_release(updown):
    if  updown == 'up':
        resume_game()


game.when_key_pressed("space").add_handler(on_space_release)
score_board.when_this_sprite_clicked().add_handler(resume_game)


