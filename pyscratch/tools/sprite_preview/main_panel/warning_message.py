from utils.render_wrapped_file_name import render_wrapped_file_name
import pyscratch as pysc
from settings import *

w, h = 400, 100
message_display = pysc.create_rect_sprite((255, 255, 255), w, h)
message_display.hide()
ori_xy = 200, 200
message_display.set_draggable(True)

def on_warning_message(message):

    message_display.show()
    message_display.set_xy(ori_xy)
    txt = render_wrapped_file_name(message, 200, DEFAULT_FONT24, color=(255,0,0))
    message_display.draw(txt, offset=(w/2, h/2))



message_display.when_receive_message('warning').add_handler(on_warning_message)

def on_click():
    message_display.hide()

message_display.when_this_sprite_clicked().add_handler(on_click)
