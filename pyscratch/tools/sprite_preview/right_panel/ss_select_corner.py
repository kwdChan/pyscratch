
import numpy as np
import pyscratch as pysc
game = pysc.game


colour = 0, 0, 0, 50

cir0 = pysc.create_circle_sprite(colour, 30)
game['c0'] = cir0

cir1 = pysc.create_circle_sprite(colour, 30)
game['c1'] = cir1

# event game start: initial setting
def on_start():

    cir0.set_draggable(True)
    cir1.set_draggable(True)

    # pysc.game.bring_to_front(cir)
    # pysc.game.bring_to_front(cir2)

    cir0.x = game['ss_view_topleft'][0] + 1
    cir0.y = game['ss_view_topleft'][1] + 1
    
    cir1.x = game['ss_view_buttom_right'][0]-1
    cir1.y = game['ss_view_buttom_right'][1]-1


    cir0.oob_limit=np.inf
    cir1.oob_limit=np.inf

game.when_game_start([cir0, cir1]).add_handler(on_start)



# useful functions
def value_if_none(v, default):
    if v is None:
        return default
    return v

def value_if_not(v, default):
    if not v:
        return default
    return v




# event game start: set the cutting offset and the frame size if the sprite is dragged
def on_start2():
    while True:
        yield 1/30
        ss_sprite: pysc.Sprite = game['ss_sprite']
        if not ss_sprite: continue
        game.bring_to_front(cir0)
        game.bring_to_front(cir1)

        mouse_down = pysc.get_mouse_presses()[0]
        if not mouse_down: 
            try:
                cir0.x = game['offset_x']*ss_sprite.scale_factor + ss_sprite.rect.left
                cir1.x = game['limit_x']*ss_sprite.scale_factor + ss_sprite.rect.left        

                cir0.y = game['offset_y']*ss_sprite.scale_factor + ss_sprite.rect.top
                cir1.y = game['limit_y']*ss_sprite.scale_factor + ss_sprite.rect.top    
            except:
                pass          
            continue
        if not (cir0.is_touching_mouse() or cir1.is_touching_mouse()): continue



        # top left of the selected rect
        cx0 = min(cir0.x, cir1.x)
        cy0 = min(cir0.y, cir1.y)
        
        # bottom right of the selected rect
        cx1 = max(cir0.x, cir1.x)
        cy1 = max(cir0.y, cir1.y)        

        # top left of the sprite sheet
        x0, y0 = ss_sprite.rect.topleft

        img_w, img_h = ss_sprite['original_width'], ss_sprite['original_height']

        # scale factor
        scale_factor = ss_sprite.scale_factor
        
        # RC
        n_col = value_if_not(game['n_col'], 1)
        n_row = value_if_not(game['n_row'], 1)

        # O
        game['offset_x'] = Ox = max(np.floor((cx0-x0)/scale_factor), 0)
        game['offset_y'] = Oy = max(np.floor((cy0-y0)/scale_factor), 0)

        # L
        game['limit_x'] = Lx = min(np.ceil((cx1-x0)/scale_factor), img_w-1)
        game['limit_y'] = Ly = min(np.ceil((cy1-y0)/scale_factor), img_h-1) 

        # update the size
        game['size_x'] = Lx - Ox + 1
        game['size_y'] = Ly - Oy + 1

        # pix
        game['pixel_x'] = np.floor(game['size_x']/n_col)
        game['pixel_y'] = np.floor(game['size_y']/n_row)





pysc.game.when_game_start([cir0, cir1]).add_handler(on_start2)


def on_offset_x_change(data):

    if not (size_x := game['size_x']): return 
    if not (offset_x := game['offset_x']): 
        game['offset_x'] = 0
        offset_x = 0         

    ss_sprite: pysc.Sprite = game['ss_sprite']
    if not ss_sprite: return 
    
    game['limit_x'] = min(size_x+offset_x-1, ss_sprite['original_width']-1)

    game['size_x'] =  game['limit_x'] - offset_x + 1

    cir0.x = offset_x*ss_sprite.scale_factor + ss_sprite.rect.left
    cir1.x = game['limit_x']*ss_sprite.scale_factor + ss_sprite.rect.left

    game['n_col'] = np.floor(game['size_x']/game['pixel_x'])

game.when_receive_message('offset_x_change').add_handler(on_offset_x_change)

def on_offset_y_change(data):

    if not (size_y := game['size_y']): return 
    if (offset_y := game['offset_y']) is None: 
        game['offset_y'] = 0
        offset_y = 0
         
    ss_sprite: pysc.Sprite = game['ss_sprite']
    if not ss_sprite: return 
    
    game['limit_y'] = min(size_y+offset_y-1, ss_sprite['original_height']-1)

    game['size_y'] =  game['limit_y'] - offset_y + 1

    cir0.y = offset_y*ss_sprite.scale_factor + ss_sprite.rect.top
    cir1.y = game['limit_y']*ss_sprite.scale_factor + ss_sprite.rect.top

    game['n_row'] = np.floor(game['size_y']/game['pixel_y'])

game.when_receive_message('offset_y_change').add_handler(on_offset_y_change)


def on_n_row_change(data):
    if not game['size_y']: return 
    game['pixel_y'] = np.floor(game['size_y']/value_if_not(game['n_row'], 1))

game.when_receive_message('n_row_change').add_handler(on_n_row_change)


def on_n_col_change(data):
    if not game['size_x']: return 
    game['pixel_x'] = np.floor(game['size_x']/value_if_not(game['n_col'], 1))

game.when_receive_message('n_col_change').add_handler(on_n_col_change)



def on_pix_x_change(data):
    if not game['size_x']: return 
    game['n_col'] = np.floor(game['size_x']/value_if_not(game['pixel_x'], 1))


game.when_receive_message('pixel_x_change').add_handler(on_pix_x_change)

def on_pix_y_change(data):
    if not game['size_y']: return 
    game['n_row'] = np.floor(game['size_y']/value_if_not(game['pixel_y'], 1))


game.when_receive_message('pixel_y_change').add_handler(on_pix_y_change)



def on_scale_change(data):
    ss_sprite: pysc.Sprite = game['ss_sprite']
    if game['offset_x'] is None: return 
    if game['limit_x'] is None: return 
    if game['offset_y'] is None: return 
    if game['limit_y'] is None: return 
    

    cir0.x = game['offset_x']*ss_sprite.scale_factor + ss_sprite.rect.left
    cir1.x = game['limit_x']*ss_sprite.scale_factor + ss_sprite.rect.left

    cir0.y = game['offset_y']*ss_sprite.scale_factor + ss_sprite.rect.top
    cir1.y = game['limit_y']*ss_sprite.scale_factor + ss_sprite.rect.top


game.when_receive_message('ss_sprite_scale_change').add_handler(on_pix_y_change)
