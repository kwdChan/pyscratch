import pygame
import numpy as np
from settings import *
import pyscratch as pysc
game = pysc.game 
xpos2 = 1050


w, h = 50*1.62, 40
colour = (255, 127, 127)
button = pysc.create_rect_sprite(colour, w, h)
button.set_xy((1200, 650))
button.write_text("Fit", DEFAULT_FONT24, offset=(w/2, h/2))
pysc.game.change_layer(button, 1)



def on_click():
    if not 'image_on_right_display' in pysc.game.shared_data:
        pysc.game.broadcast_message('warning', 'image not selected' )
        return 
            
    if game['offset_x'] is None: return 
    if game['offset_y'] is None: return 
    if game['size_x'] is None: return 
    if game['size_y'] is None: return 


    img: pygame.Surface = game['image_on_right_display']


    fitter = ParamsFitter(img)

    n_col, pixel_x, offset_x = fitter.find_best_x(game['offset_x'], game['limit_x'])
    n_row, pixel_y, offset_y = fitter.find_best_y(game['offset_y'], game['limit_y'])

    if (n_col and pixel_x and (not offset_x is None)):
        game['n_col'] = n_col
        game['pixel_x'] = pixel_x
        game['offset_x'] = offset_x
        game['size_x'] = min(game['limit_x'] - game['offset_x']+1, game['size_x'])

    if (n_row and pixel_y and (not offset_y is None)):
        game['n_row'] = n_row
        game['pixel_y'] = pixel_y
        game['offset_y'] = offset_y
        game['offset_y'] = offset_y
        game['size_y'] = min(game['limit_y'] - game['offset_y']+1, game['size_y'])


    #game.broadcast_message('n_row_change')
    #game.broadcast_message('n_col_change')

    #game.broadcast_message('pixel_x_change')

    #game.broadcast_message('pixel_y_change')

    #game.broadcast_message('offset_x_change')
    #game.broadcast_message('offset_y_change')

    


button.when_this_sprite_clicked().add_handler(on_click)

from itertools import product
class ParamsFitter:

    def __init__(self, surface):

        self.surface = surface
        self.arr = pygame.surfarray.pixels_alpha(surface)

        self.yslits = ParamsFitter.get_slit_values(self.arr.mean(0))
        self.xslits = ParamsFitter.get_slit_values(self.arr.mean(1))
    
    def num_frames_x(self, offset, limit):
        # TODO: think about it: is the boundary correct?
        return ParamsFitter.get_num_frames(self.xslits[offset: limit+2])
    
    def num_frames_y(self, offset, limit):
        return ParamsFitter.get_num_frames(self.yslits[offset: limit+2])
    
    def find_best_x(self, offset_centre: int, limit:int):
        offset_centre = int(offset_centre)
        limit = int(limit)

        return ParamsFitter.search_best(self.xslits[: limit+2], offset_centre)
    
    def find_best_y(self, offset_centre: int, limit:int):
        offset_centre = int(offset_centre)
        limit = int(limit)
        return ParamsFitter.search_best(self.yslits[: limit+2], offset_centre)
    
    @staticmethod
    def search_best(slit_values, centre_offset, step_range_ratio=0.1, offset_range_ratio=0.1):
        #print(len(slit_values))
        n_frame = int(ParamsFitter.get_num_frames(slit_values[centre_offset:]))
        print(ParamsFitter.get_num_frames_rank(slit_values[centre_offset:]))

        # TODO: possibly DIV BY ZERO?
        step_size = max(1, (len(slit_values[centre_offset:])-1)/n_frame )
        
        step_range = round(step_size*step_range_ratio)
        offset_range = round(step_size*offset_range_ratio)

        step_size = round(step_size)

        # TODO: very easy to go out of boundary
        step_sizes = range(step_size+step_range+1, max(0, step_size-step_range), -1)
        offsets = range(max(0,centre_offset-offset_range), centre_offset+offset_range+1)

        vmin = np.inf
        best_ss = None
        best_os = None
        for ss, os in product(step_sizes, offsets):

            n, v = ParamsFitter.eval_cut(slit_values, ss, os)
            #print(f"trying: pixel_sz:{ss}, offset:{os} -> {n, v}")
            if not n == n_frame: continue
            if v < vmin:
                best_ss = ss
                best_os = os
                vmin = v
            #print(ss, os, v)



        print(f"n_frame: {n_frame}, pixel_sz:{best_ss}, offset:{best_os} -> {vmin}")
        return n_frame, best_ss, best_os
        
    @staticmethod
    def get_num_frames(slit_values):
        return np.argmax(np.abs(np.fft.fft(slit_values))[1:len(slit_values)//2])+1 
        
    @staticmethod
    def get_num_frames_rank(slit_values):
        return np.argsort(np.abs(np.fft.fft(slit_values))[1:len(slit_values)//2])+1 
    

    @staticmethod
    def get_rough_est_num_pixel(slit_values):
        return (len(slit_values)-1)/ParamsFitter.get_num_frames(slit_values)

    @staticmethod
    def eval_cut(slit_values, step_size, offset=0):
        cut_indices = np.arange(offset, len(slit_values), step_size)
        return len(cut_indices)-1, slit_values[cut_indices].mean()   
 
    @staticmethod
    def get_slit_values(axis_mean):
        return np.r_[[0], (axis_mean[1:]+axis_mean[:-1]), [0]]
