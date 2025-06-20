"""
broadcast messages: 
    scrolling (scrolling_offset)

shared_data:
    scrolling_offset
"""


from pathlib import Path
from typing import Dict

from pygame import Surface
import pyscratch as pysc
from settings import *



# Sprite: the panel (the background of the preview frames)
PANEL_BG_COLOUR = 199, 207, 224
panel = pysc.create_rect_sprite(
    PANEL_BG_COLOUR,
    LEFT_PANEL_WIDTH, 
    SCREEN_HEIGHT# - PANEL_MARGIN*2
)
panel.set_xy((LEFT_PANEL_WIDTH/2,  SCREEN_HEIGHT/2))

# event: scrolling
pysc.game['scrolling_offset'] = 0
def on_mouse_scroll(updown):
    if not panel.is_touching_mouse(): return
    if updown == 'up':
        pysc.game['scrolling_offset'] += 10
    else: 

        pysc.game['scrolling_offset'] -= 10
        
    pysc.game.broadcast_message("scrolling", pysc.game['scrolling_offset'])
    
pysc.game.when_mouse_scroll().add_handler(on_mouse_scroll)
pysc.game['left_panel'] = panel

