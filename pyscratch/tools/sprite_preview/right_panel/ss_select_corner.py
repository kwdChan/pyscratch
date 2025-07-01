import pyscratch as pysc

colour = 0, 0, 0, 50

cir = pysc.create_circle_sprite(colour, 30)
pysc.game['ss_select_corner1'] = cir

cir2 = pysc.create_circle_sprite(colour, 30)
pysc.game['ss_select_corner2'] = cir2

# event game start: initial setting
def on_start():

    cir.set_draggable(True)
    cir2.set_draggable(True)

    pysc.game.bring_to_front(cir)
    pysc.game.bring_to_front(cir2)

    cir.x = pysc.game['ss_view_topleft'][0] + 1
    cir.y = pysc.game['ss_view_topleft'][1] + 1
    
    cir2.x = pysc.game['ss_view_buttom_right'][0]-1
    cir2.y = pysc.game['ss_view_buttom_right'][1]-1

pysc.game.when_game_start([cir, cir2]).add_handler(on_start)

pysc.game['x1'] = None
pysc.game['y1'] = None
# event game start: set the cutting offset and the frame size if the sprite is dragged
def on_start2():
    while True:
        yield 1/30
        mouse_down = pysc.get_mouse_presses()[0]
        if mouse_down and (cir.is_touching_mouse() or cir2.is_touching_mouse()):
            if (ss_sprite := pysc.game['ss_sprite']):
                topleft = ss_sprite.rect.topleft
                bottomright = ss_sprite.rect.bottomright
            else:
                topleft = -10000, -10000
                bottomright = 10000, 10000


            n_col = 1 if not pysc.game['n_col'] else pysc.game['n_col']
            n_row = 1 if not pysc.game['n_row'] else pysc.game['n_row']
            x0 = max(min(cir.x, cir2.x), topleft[0])
            y0 = max(min(cir.y, cir2.y), topleft[1])

            x1 = min(max(cir.x, cir2.x), bottomright[0])
            y1 = min(max(cir.y, cir2.y), bottomright[1])


            pysc.game['offset_x'] = x0-topleft[0]
            pysc.game['offset_y'] = y0-topleft[1]

            pysc.game['pixel_x'] = (x1-x0)//n_col
            pysc.game['pixel_y'] = (y1-y0)//n_row

            pysc.game['x0'] = x0
            pysc.game['y0'] = y0

            pysc.game['x1'] = x1
            pysc.game['y1'] = y1

pysc.game.when_game_start([cir, cir2]).add_handler(on_start2)

def value_if_none(v, default):
    if v is None:
        return default
    return v

def value_if_not(v, default):
    if not v:
        return default
    return v



def on_offset_change(data):
    offset_x = value_if_none(pysc.game['offset_x'], 0)
    offset_y = value_if_none(pysc.game['offset_y'], 0)

    n_col = value_if_not(pysc.game['n_col'], 1)
    n_row = value_if_not(pysc.game['n_row'], 1)

    pixel_x = value_if_none(pysc.game['pixel_x'], 1)
    pixel_y = value_if_none(pysc.game['pixel_y'], 1)




def on_parameter_changes(data):

    if (ss_sprite := pysc.game['ss_sprite']):
        topleft = ss_sprite.rect.topleft
        bottomright = ss_sprite.rect.bottomright

        offset_x = value_if_none(pysc.game['offset_x'], 0)
        offset_y = value_if_none(pysc.game['offset_y'], 0)

        n_col = value_if_not(pysc.game['n_col'], 1)
        n_row = value_if_not(pysc.game['n_row'], 1)

        pixel_x = value_if_none(pysc.game['pixel_x'], ss_sprite.rect.width)
        pixel_y = value_if_none(pysc.game['pixel_y'], ss_sprite.rect.height)


        cir.x = offset_x+topleft[0]
        cir.y = offset_y+topleft[1]

        pysc.game['x0'] = cir.x
        pysc.game['y0'] = cir.y



        cir2.x = cir.x+n_col*pixel_x
        cir2.y = cir.y+n_row*pixel_y

        pysc.game['x1'] = cir2.x
        pysc.game['y1'] = cir2.y
        


#pysc.game.when_receive_message('n_col_change').add_handler(on_parameter_changes)
#pysc.game.when_receive_message('n_row_change').add_handler(on_parameter_changes)
pysc.game.when_receive_message('pixel_x_change').add_handler(on_parameter_changes)
pysc.game.when_receive_message('pixel_y_change').add_handler(on_parameter_changes)
pysc.game.when_receive_message('offset_x_change').add_handler(on_parameter_changes)
pysc.game.when_receive_message('offset_y_change').add_handler(on_parameter_changes)



