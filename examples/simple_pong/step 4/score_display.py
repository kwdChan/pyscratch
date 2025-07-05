import pyscratch as pysc
import pygame
game = pysc.game

# 
font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size
game['left_score'] = 0
game['right_score'] = 0
game['running'] = False

width = 150
height = 70


# sprites
score_board = pysc.create_rect_sprite((200, 200, 200), width, height)


# set the position of the score board
def set_position_on_game_start():
    score_board.x = game['SCREEN_WIDTH']/2
    score_board.y = game['SCREEN_HEIGHT']/2

score_board.when_game_start().add_handler(set_position_on_game_start)


# display the score 
def display_score():
    score_board.show()
    text = f'{game['left_score'] } - {game['right_score'] }'
    score_board.write_text(text, font, offset=(width/2, height/2))

score_board.when_game_start().add_handler(display_score)


# left score
def on_left_score(data):
    game['left_score'] += 1 
    game['running'] = False

    display_score() # call the display function

score_board.when_receive_message('left_score').add_handler(on_left_score)

# right score
def on_right_score(data):
    game['right_score'] += 1 
    game['running'] = False

    display_score() # call the display function

score_board.when_receive_message('right_score').add_handler(on_right_score)


# resume the game when the score board is clicked
def resume_game():
    game['running'] = True
    game._hide_sprite(score_board)

score_board.when_this_sprite_clicked().add_handler(resume_game)


# also resume the game when the space is released
def on_space_release(key, updown):
    if key == 'space' and updown == 'up':
        resume_game()

game.when_any_key_pressed().add_handler(on_space_release)





