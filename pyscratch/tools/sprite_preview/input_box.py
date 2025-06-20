from calendar import Day
import pyscratch as pysc
from settings import *

w, h = 120, 40
selected_colour = (255, 255, 255)
deselected_colour = (127, 127, 127)


def FloatInputBox(data_key, message_on_change="", default_value=""):
    label = pysc.create_rect_sprite(deselected_colour, w, h)
    label.write_text(data_key, DEFAULT_FONT24, offset=(w/2, h/2))

    selected_sur = pysc.create_rect(selected_colour, w, h)
    deselected_sur = pysc.create_rect(deselected_colour, w, h)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')
    label.lock_to(text_box, (0,0), reset_xy=True)
    label.y = -h

    # def on_click():
    #     text_box.set_frame_mode('selected')
    #     text_box.private_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box['selected'] = False
    text_box['text'] = default_value
    try:
        pysc.game.shared_data[data_key] = float(text_box.private_data['text'])
    except:
        pysc.game.shared_data[data_key] = None    

    text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.private_data['selected']: return
        if text_box['just_selected']: 
            text_box['just_selected'] = False
            text_box['text'] = ''

        if key.isdigit() or key == '.':
            text_box.private_data['text'] += key

        if key == 'backspace' and len(text_box.private_data['text']):
            text_box.private_data['text'] = text_box.private_data['text'][:-1]

        try:
            pysc.game.shared_data[data_key] = float(text_box.private_data['text'])
        except:
            pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.private_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))

        if message_on_change:
            pysc.game.broadcast_message(message_on_change, pysc.game.shared_data[data_key])
            
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            text_box.private_data['selected'] = False
            text_box['just_selected'] = False
            text_box.set_frame_mode('deselected')
            text_box.write_text(text_box.private_data['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))

        else:
            text_box.private_data['selected'] = True
            text_box['just_selected'] = True
            text_box.set_frame_mode('selected')
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)

    return text_box

def IntegerInputBox(data_key):
    wl = 60
    label = pysc.create_rect_sprite(deselected_colour, wl, h)
    label.write_text(data_key, DEFAULT_FONT24, offset=(wl/2, h/2))

    selected_sur = pysc.create_rect(selected_colour, w, h)
    deselected_sur = pysc.create_rect(deselected_colour, w, h)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')
    label.lock_to(text_box, (0,0), reset_xy=True)
    label.x = -w/2-wl/2

    # def on_click():
    #     text_box.set_frame_mode('selected')
    #     text_box.private_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box.private_data['selected'] = False
    text_box.private_data['text'] = ""
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.private_data['selected']: return
        if text_box['just_selected']: 
            text_box['just_selected'] = False
            text_box['text'] = ''

        if key.isdigit():
            text_box.private_data['text'] += key

        if key == 'backspace' and len(text_box.private_data['text']):
            text_box.private_data['text'] = text_box.private_data['text'][:-1]

        try:
            pysc.game.shared_data[data_key] = int(text_box.private_data['text'])
        except:
            pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.private_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))

        
        
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            text_box['selected'] = False
            text_box['just_selected'] = False
            text_box.set_frame_mode('deselected')
            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))

        else:
            text_box['selected'] = True
            text_box['just_selected'] = True
            text_box.set_frame_mode('selected')
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)

    return text_box