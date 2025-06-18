from pathlib import Path
from typing import Dict

from pygame import Surface
import pyscratch as pysc
from settings import *


pysc.game.shared_data['display_sprite'] = None


def create_display_sprite(frames):

    #frame_list = [c['surface'] for c in pysc.game['frame_card_list']]
    #print(frames)
    if pysc.game['display_sprite']:
        pysc.game['display_sprite'].remove()

    if not len(frames):
        pysc.game['display_sprite'] = None
        return


    sprite = pysc.Sprite({'always':frames})
    sprite.set_xy((200, 200))

    if pysc.game['scale_factor']:
        sprite.set_scale(pysc.game['scale_factor'])

    pysc.game['display_sprite'] = sprite

    def play(_):
        while True:
            itv = pysc.game['frame_interval']
            if pysc.game['is_playing'] and itv:
                sprite.next_frame()
            yield itv if itv else 0.1

    sprite.when_timer_above(0).add_handler(play)


    def on_scale_factor_change(scale):
        print(scale)
        if scale: 
            sprite.set_scale(scale)

    sprite.when_receive_message("scale_factor_change").add_handler(on_scale_factor_change)
    sprite.when_receive_message('preview_click').add_handler(lambda d: sprite.set_frame(d['order']))



pysc.game.when_receive_message("change_animation_done").add_handler(create_display_sprite)