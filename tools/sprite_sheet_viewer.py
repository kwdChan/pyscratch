from anyio import SpooledTemporaryFile
from scratch_sprite import ScratchSprite, circle_sprite, rect_sprite
import pygame
import pymunk
from game import game # neccessary for image loading
from helper import scale_to_fit_aspect, scale_and_tile, scale_to_fill_screen, adjust_brightness, set_transparency

from helper import get_frame, get_frame_sequence, get_frame_dict
import scratch_sprite
import sensing

w, h = 2300, 1000
game.update_screen_mode((2300, 1000))
sprite_sheet_img = pygame.image.load("assets/Danmaku/Shot_01.png").convert_alpha()
img_width, img_height = sprite_sheet_img.get_width(), sprite_sheet_img.get_height()

sprite_sheet = ScratchSprite({'always': [sprite_sheet_img]},'always', (0+img_width//2, 0+img_height//2))
game.add_sprite(sprite_sheet)


def move_sheet_by_xy():
    pass


trigger = game.create_timer_trigger(1000/120)
def forever(_):
    if sensing.is_key_pressed(['up']):
        sprite_sheet.move_xy((0, 3))

    if sensing.is_key_pressed(['down']):
        sprite_sheet.move_xy((0, -3))

    if sensing.is_key_pressed(['left']):
        sprite_sheet.move_xy((3, 0))

    if sensing.is_key_pressed(['right']):
        sprite_sheet.move_xy((-3, 0))


trigger.on_reset(forever)



key_trigger = game.create_key_trigger()
def on_key_event(key, updown):
    if updown == 'up': return

    if key == '=':
        sprite_sheet.scale_by(2)


    if key == '-':
        sprite_sheet.scale_by(1/2)



key_trigger.add_callback(on_key_event)

game.start(60, sim_step_min=60, debug_draw=False)
