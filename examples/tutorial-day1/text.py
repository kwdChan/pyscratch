import pyscratch as pysc
import pygame
game = pysc.game

text_box = pysc.create_rect_sprite((200, 200, 200, 20), 700, 90)
font = pygame.font.Font('assets/Kenney Future.ttf', size=96)

text_box.write_text("YOU LOSE", font, offset=(350, 45))


text_box.hide()

text_box.set_draggable(True)
text_box.set_xy((260, 195))
text_box.direction = -35



def game_end(): 
    text_box.show()

text_box.when_backdrop_switched(1).add_handler(game_end)

