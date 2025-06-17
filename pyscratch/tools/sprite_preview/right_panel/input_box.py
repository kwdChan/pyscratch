import pyscratch as pysc
from settings import *

w, d = 100, 40
selected_colour = (255, 255, 255)
deselected_colour = (127, 127, 127)

def NumberInputBox(data_key):
    selected_sur = pysc.create_rect(selected_colour, w, d)
    deselected_sur = pysc.create_rect(deselected_colour, w, d)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')

    # def on_click():
    #     text_box.set_frame_mode('selected')
    #     text_box.private_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box.private_data['selected'] = False
    text_box.private_data['text'] = ""
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.private_data['selected']: return
        if key.isdigit():
            text_box.private_data['text'] += key

        if key == 'backspace' and len(text_box.private_data['text']):
            text_box.private_data['text'] = text_box.private_data['text'][:-1]

        try:
            pysc.game.shared_data[data_key] = int(text_box.private_data['text'])
        except:
            pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.private_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, d/2))

        
        
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            text_box.private_data['selected'] = False
            text_box.set_frame_mode('deselected')
            text_box.write_text(text_box.private_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, d/2))

        else:
            text_box.private_data['selected'] = True
            text_box.set_frame_mode('selected')
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)

    return text_box