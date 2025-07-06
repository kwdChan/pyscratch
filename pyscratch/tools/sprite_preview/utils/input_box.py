from calendar import Day
import pyscratch as pysc
from settings import *

w, h = 120, 40
selected_colour = (255, 255, 255)
deselected_colour = (127, 127, 127)


def FloatInputBoxVerticallyLabel(data_key, message_on_change="", default_value=""):
    label = pysc.create_rect_sprite(deselected_colour, w, h)
    label.write_text(data_key, DEFAULT_FONT24, offset=(w/2, h/2))

    selected_sur = pysc.create_rect(selected_colour, w, h)
    deselected_sur = pysc.create_rect(deselected_colour, w, h)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')
    label.lock_to(text_box, (0,0), reset_xy=True)
    label.y = -h

    # def on_click():
    #     text_box.set_animation('selected')
    #     text_box.sprite_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box['selected'] = False
    text_box['text'] = default_value
    try:
        pysc.game.shared_data[data_key] = float(text_box.sprite_data['text'])
    except:
        pysc.game.shared_data[data_key] = None    

    text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.sprite_data['selected']: return
        if text_box['just_selected']: 
            text_box['just_selected'] = False
            text_box['text'] = ''

        if key.isdigit() or key == '.':
            text_box.sprite_data['text'] += key

        if key == 'backspace' and len(text_box.sprite_data['text']):
            text_box.sprite_data['text'] = text_box.sprite_data['text'][:-1]

        try:
            pysc.game.shared_data[data_key] = float(text_box.sprite_data['text'])
        except:
            pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.sprite_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))

        if message_on_change:
            pysc.game.broadcast_message(message_on_change, pysc.game.shared_data[data_key])
            
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            text_box.sprite_data['selected'] = False
            text_box['just_selected'] = False
            text_box.set_animation('deselected')
            text_box.write_text(text_box.sprite_data['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))

        else:
            text_box.sprite_data['selected'] = True
            text_box['just_selected'] = True
            text_box.set_animation('selected')
            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)

    return text_box


def FloatInputBoxHoriLabel(data_key, message_on_change="", default_value="", label_width=80):
    wl = label_width
    label = pysc.create_rect_sprite(deselected_colour, wl, h)
    label.write_text(data_key, DEFAULT_FONT24, offset=(wl/2, h/2))

    selected_sur = pysc.create_rect(selected_colour, w, h)
    deselected_sur = pysc.create_rect(deselected_colour, w, h)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')
    label.lock_to(text_box, (0,0), reset_xy=True)
    label.x = -w/2-wl/2


    # def on_click():
    #     text_box.set_animation('selected')
    #     text_box.sprite_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box['selected'] = False
    text_box['text'] = default_value
    try:
        pysc.game.shared_data[data_key] = float(text_box.sprite_data['text'])
    except:
        pysc.game.shared_data[data_key] = None    

    text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.sprite_data['selected']: return
        if text_box['just_selected']: 
            text_box['just_selected'] = False
            text_box['text'] = ''

        if key.isdigit() or key == '.':
            text_box.sprite_data['text'] += key

        if key == 'backspace' and len(text_box.sprite_data['text']):
            text_box.sprite_data['text'] = text_box.sprite_data['text'][:-1]

        try:
            pysc.game.shared_data[data_key] = float(text_box.sprite_data['text'])
        except:
            pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.sprite_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))

        if message_on_change:
            pysc.game.broadcast_message(message_on_change, pysc.game.shared_data[data_key])
            
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            text_box.sprite_data['selected'] = False
            text_box['just_selected'] = False
            text_box.set_animation('deselected')
            text_box.write_text(text_box.sprite_data['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))

        else:
            text_box.sprite_data['selected'] = True
            text_box['just_selected'] = True
            text_box.set_animation('selected')
            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)

    return text_box


def IntegerInputBox(data_key, message_on_change="", default_value="", label_width=60):
    wl = label_width
    label = pysc.create_rect_sprite(deselected_colour, wl, h)
    label.write_text(data_key, DEFAULT_FONT24, offset=(wl/2, h/2))

    selected_sur = pysc.create_rect(selected_colour, w, h)
    deselected_sur = pysc.create_rect(deselected_colour, w, h)
    pysc.game.shared_data[data_key] = None
    text_box = pysc.Sprite({'selected':[selected_sur], 'deselected':[deselected_sur]}, 'deselected')
    label.lock_to(text_box, (0,0), reset_xy=True)
    label.x = -w/2-wl/2

    # def on_click():
    #     text_box.set_animation('selected')
    #     text_box.sprite_data['selected'] = True

    # text_box.when_this_sprite_clicked().add_handler(on_click)
    text_box.sprite_data['selected'] = False
    text_box.sprite_data['text'] = default_value
    text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))
    def on_any_key_press(key:str, updown):
        if updown == 'up': return
        if not text_box.sprite_data['selected']: return
        if text_box['just_selected']: 
            text_box['just_selected'] = False
            text_box['text'] = ''

        if key.isdigit():
            text_box.sprite_data['text'] += key

        if key == 'backspace' and len(text_box.sprite_data['text']):
            text_box.sprite_data['text'] = text_box.sprite_data['text'][:-1]

        # try:
        #     pysc.game.shared_data[data_key] = int(text_box.sprite_data['text'])
        # except:
        #     pysc.game.shared_data[data_key] = None
        
        text_box.write_text(text_box.sprite_data['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))

        
        
    text_box.when_any_key_pressed().add_handler(on_any_key_press)

    def on_any_mouse_click(pos, button, updown):
        if not text_box.is_touching_mouse():
            #print(button)
            #print(pos)
            if text_box['selected']:
                try:
                    pysc.game.shared_data[data_key] = int(text_box.sprite_data['text'])
                except:
                    pysc.game.shared_data[data_key] = None
                if message_on_change:
                    pysc.game.broadcast_message(message_on_change, pysc.game.shared_data[data_key])
            text_box['selected'] = False
            text_box['just_selected'] = False
            text_box.set_animation('deselected')
            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))

        else:
            text_box['selected'] = True
            text_box['just_selected'] = True
            text_box.set_animation('selected')
            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(0,0,0), offset=(w/2, h/2))
    pysc.game.when_mouse_click([text_box]).add_handler(on_any_mouse_click)


    def update_value_on_change():
        while True:
            yield 1/30

            

            if text_box.animation_name == "selected":
                continue

            try: 
                text_box['text'] = str(round(pysc.game[data_key]))
            except:
                text_box['text'] = ""

            text_box.write_text(text_box['text'], DEFAULT_FONT24, colour=(255,255,255), offset=(w/2, h/2))


    text_box.when_game_start().add_handler(update_value_on_change)

    return text_box