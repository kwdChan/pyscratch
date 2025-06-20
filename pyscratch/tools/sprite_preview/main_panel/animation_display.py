"""
shared_data:
    display_sprite
    scale_factor
    frame_interval
    is_playing

receive messages:
    preview_click
        change the frame of the display sprite when the preview is clicked

    scale_factor_change
        change the scale of the display sprite    
    
    change_animation_done
        destory and create the display sprite for a new animation
"""

from pathlib import Path
from typing import Dict

from pygame import Surface
import pyscratch as pysc
from settings import *


pysc.game['display_sprite'] = None


def create_display_sprite(frames):

    #frame_list = [c['surface'] for c in pysc.game['frame_card_list']]
    #print(frames)
    if display_sprite:=pysc.game['display_sprite']:
        display_sprite.remove()
        x, y = display_sprite.x, display_sprite.y
    else:
        x, y = 350, 200

    if not len(frames):
        pysc.game['display_sprite'] = None
        return


    sprite = pysc.Sprite({'always':frames})
    sprite.set_xy((x, y))
    
    sprite.set_draggable(True)

    if pysc.game['scale_factor']:
        sprite.set_scale(pysc.game['scale_factor'])

    pysc.game['display_sprite'] = sprite

    def play(_):
        #TODO: if the user put a big value in frame_interval, and change it back to a small one
        # the animation will wait for the big frame_interval until it comes back again 
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