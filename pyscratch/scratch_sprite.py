from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Hashable, Iterable, List, Optional, ParamSpec, Tuple, Union, cast, override
import numpy as np
import pygame 
import pymunk

from pyscratch import sensing
from .game import Game, game
from .helper import adjust_brightness, set_transparency, create_rect, create_circle, load_frames_from_folder
from pathlib import Path

class RotationStyle(Enum):
    ALL_AROUND = 0
    LEFTRIGHT = 1
    FIXED = 2


def create_animated_sprite(folder_path,  *args, **kwargs):
    frame_dict = load_frames_from_folder(folder_path)
    return ScratchSprite(frame_dict, *args, **kwargs)


def create_single_costume_sprite(image_path, *args, **kwargs):
    img = pygame.image.load(image_path).convert_alpha()
    frame_dict = {"always": [img]}
    return ScratchSprite(frame_dict, *args, **kwargs)


def create_shared_data_display_sprite(key, font, size = (150, 50), colour=(127, 127, 127), position: Optional[Tuple[float, float]]=None, **kwargs):

    w, h = size
    if position is None:
        position = w/2+25, h/2+25
    sprite = create_rect_sprite(colour, w, h, pos=position, **kwargs)

    def keep_score():
        while True: 
            sprite.write_text(f"{key}: {game.shared_data[key]}", font=font, offset=(w/2, h/2))
            yield 100

    sprite.when_game_start().add_callback(keep_score)
    return sprite

def create_circle_sprite(colour, radius, *args, **kwargs):
    circle = create_circle(colour, radius)
    return ScratchSprite({"always":[circle]}, "always", *args, **kwargs)


def create_rect_sprite(colour, width, height, *args, **kwargs):
    rect = create_rect(colour, width, height)
    return ScratchSprite({"always":[rect]}, "always", *args, **kwargs)


def create_edge_sprites(edge_colour = (255, 0, 0), thickness=4, collision_type=1, game=game):
    # TODO: make the edge way thicker to avoid escape due to physics inaccuracy 
    # edges
    edge_body = pymunk.Body.STATIC
    screen_w, screen_h = game.screen.get_width(), game.screen.get_height()

    top_edge = create_rect_sprite(edge_colour, screen_w, thickness, (screen_w//2, 0),body_type= edge_body)
    bottom_edge = create_rect_sprite(edge_colour, screen_w, thickness, (screen_w//2, screen_h),body_type= edge_body)
    left_edge = create_rect_sprite(edge_colour, thickness, screen_h, (0, screen_h//2),body_type= edge_body)
    right_edge = create_rect_sprite(edge_colour, thickness, screen_h, (screen_w,  screen_h//2),body_type= edge_body)

    top_edge.set_collision_type(collision_type)
    bottom_edge.set_collision_type(collision_type)
    left_edge.set_collision_type(collision_type)
    right_edge.set_collision_type(collision_type)

    #game.add_sprite(top_edge)
    #game.add_sprite(bottom_edge)
    #game.add_sprite(left_edge)
    #game.add_sprite(right_edge)

    return top_edge, left_edge, bottom_edge, right_edge


class ScratchSprite(pygame.sprite.Sprite):
    
    def __init__(self, frame_dict: Dict[str, List[pygame.Surface]], starting_mode:Optional[str]=None, pos= (100, 100), shape_type='circle', shape_factor=0.8, body_type=pymunk.Body.KINEMATIC):
        # DYNAMIC, KINEMATIC, STATIC

        super().__init__()

        #frame_dict = {k: [i.copy() for i in v] for k, v in frame_dict.items()}
        self.frame_dict_original:Dict[str, List[pygame.Surface]] = {k: [i.copy() for i in v] for k, v in frame_dict.items()} # never changed
        self.frame_dict:Dict[str, List[pygame.Surface]] = {k: [i.copy() for i in v] for k, v in frame_dict.items()} # transformed on the spot

        self.frames: List[pygame.Surface] # updated on the spot
        self.frame_mode: str
        self.frame_idx: int
        
        if starting_mode is None:
            starting_mode = list(self.frame_dict.keys())[0]  # there must be at least one frame in the frame_dict so assuming index 0 is okay

        self.set_frame_mode(starting_mode)
        self.set_frame(0)

        self.body = pymunk.Body(1, 100, body_type=body_type)

        self.body.position = pos # change be updated anytime 

        self.shape: pymunk.Shape # swapped only during self.update
        self.new_shape: Optional[pymunk.Shape] # swapped only during self.update

        self.image: pygame.Surface # rotated and flipped every update during self.update
        self.rect: pygame.Rect # depends on the rotated image and thus should be redefined during self.update


        
        self.scale_factor = 1

        self.set_shape(shape_type, shape_factor)
        self.shape, self.new_shape = cast(pymunk.Shape, self.new_shape), None

        self.mouse_selected = False
        self.is_dragging = False
        self.draggable = False
        self.elasticity: float = .99
        self.friction: float = 0

        self.private_data = {}
        self.flip_y = False
        self.flip_x = False
        self.transparency_factor = 1.0
        self.brightness_factor = 1.0

        self.lock_to_sprite = None
        self.lock_offset = 0, 0

        self.collision_type:int = 1


        self.rotation_style: RotationStyle = RotationStyle.ALL_AROUND

        game.add_sprite(self)

    def is_mouse_selected(self):
        return self.mouse_selected
    
    def set_draggable(self, draggable):
        self.draggable = draggable

    def set_is_dragging(self, is_dragging):
        self.is_dragging = is_dragging

    def set_frame_mode(self, new_mode):
        self.frame_mode = new_mode
        self.frames = self.frame_dict[new_mode]
        self.set_frame(0)

    def flip_horizontal(self):
        self.flip_x = not self.flip_x

    def flip_vertical(self):
        self.flip_y = not self.flip_y

    @override
    def update(self, space):

        if self.lock_to_sprite:
            self.body.position = self.lock_to_sprite.body.position + self.lock_offset
            self.body.velocity = 0, 0 

        x, y = self.body.position
        img = self.frames[self.frame_idx]

        self_angle = self.body.rotation_vector.angle_degrees
        if self.rotation_style == RotationStyle.ALL_AROUND: 
            img = pygame.transform.rotate(img, -self_angle)
    
        elif self.rotation_style == RotationStyle.LEFTRIGHT:
            if self_angle > -90 and self_angle < 90:
                pass
            else:
                img = pygame.transform.flip(img, True, False)
             
        elif self.rotation_style == RotationStyle.FIXED:
            pass

        
        img = pygame.transform.flip(img, self.flip_x, self.flip_y)


        self.image = img

        img_w, img_h = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect(
            center=(x, y),
              width=img_w,
              height=img_h,
              )


        if self.new_shape: 
            game.cleanup_old_shape(self.shape)

            space.remove(self.shape)
            self.shape, self.new_shape = self.new_shape, None
            self.shape.elasticity = self.elasticity
            self.shape.friction = self.friction

            space.add(self.shape)

        if self.is_dragging:
            self.body.velocity=0,0 
            # TODO: should be done every physics loop or reset location every frame
            # or can i change it to kinamatic temporarily


    def set_mass(self, mass):
        self.body.mass = mass

    def set_moment(self, moment):
        self.body.moment = moment

    def set_elasticity(self, elasticity):
        self.elasticity = elasticity

    def set_friction(self, friction):
        self.friction = friction
    
    def set_shape(self, shape_type='circle', shape_factor=0.8, collision_allowed=False):
        # could be a function or a string
        # TODO: raise error when invalid mode is selected
        self.shape_type = shape_type
        self.shape_factor = shape_factor
        if not collision_allowed:
            self.set_collision_type(0)
        else: 
            self.set_collision_type(self.collision_type)


    def set_collision_type(self, value: int=0):
        self.collision_type = value
        self.__request_update_shape()


    def __request_update_shape(self):
        """create the shape based on the self.frames and put it in self.new_shape"""

        # the rect of the un
        rect = self.frames[self.frame_idx].get_rect()
        width = int(rect.width*self.shape_factor)
        height = int(rect.height*self.shape_factor)
        

        if self.shape_type == 'box': 
            self.new_shape = pymunk.Poly.create_box(self.body, (width, height))

        elif self.shape_type == 'circle':
            radius = (width+height)//4
            self.new_shape = pymunk.Circle(self.body,radius)

        elif self.shape_type == 'circle_width':
            self.new_shape = pymunk.Circle(self.body, rect.width//2)

        elif self.shape_type == 'circle_height':
            self.new_shape = pymunk.Circle(self.body, height//2)
        

        if self.new_shape:
            self.new_shape.collision_type = self.collision_type

        else:
            raise ValueError('invalid shape_type')




    def set_scale(self, factor):
        self.scale_factor = factor

        for k, frames in self.frame_dict_original.items():
            self.frame_dict[k] = [
                pygame.transform.scale_by(
                    adjust_brightness(
                        set_transparency(f, self.transparency_factor), 
                        self.brightness_factor),
                    factor) 
                for f in frames]

        # 
        self.set_frame_mode(self.frame_mode)
        self.__request_update_shape()

    def set_brightness(self, factor):
        self.brightness_factor = factor
        self.set_scale(self.scale_factor)

    def set_transparency(self, factor):
        self.transparency_factor = factor
        self.set_scale(self.scale_factor)

    
    def scale_by(self, factor):
        self.set_scale(self.scale_factor*factor)

    def write_text(self, text: str, font: pygame.font.Font, colour=(255,255,255), offset=(0,0)):
        text_surface = font.render(text, True, colour)  # White text
        w, h = text_surface.get_width(), text_surface.get_height()

        self.blit(text_surface, (offset[0]-w/2, offset[1]-h/2))
        
    def restore_frame(self):
        pass


    def blit(self, surface: pygame.Surface, offset=(0,0), reset=True):
        if reset: 
            self.frames[self.frame_idx] = self.frame_dict_original[self.frame_mode][self.frame_idx].copy()
        self.frames[self.frame_idx].blit(surface, offset)

    @property
    def direction(self):
        return self.body.rotation_vector.angle_degrees
    
    @direction.setter
    def direction(self, degree):
        self.set_rotation(degree)
    
    @property
    def x(self):
        return self.body.position[0]
    
    @property
    def y(self):
        return self.body.position[1]
    
    @x.setter
    def x(self, v):
        self.body.position =  v, self.body.position[1]
    
    @y.setter
    def y(self, v):
        self.body.position = self.body.position[0], v

    def get_rotation(self):
        return self.body.rotation_vector.angle_degrees
    
    def set_rotation(self, degree):
        self.body.angle = degree/180*np.pi

    def add_rotation(self, degree):
        self.body.angle += degree/180*np.pi

    def set_frame(self, idx):
        self.frame_idx = idx
    
    def next_frame(self):
        self.set_frame((self.frame_idx+1) % len(self.frames))


    def move_indir(self, length):
        self.body.position += self.body.rotation_vector*length
        
    def move_across_dir(self, length):
        self.body.position += self.body.rotation_vector.perpendicular()*length
        

    def move_xy(self, xy):
        self.body.position = self.body.position + xy


    def set_xy(self, xy):
        self.body.position =  xy


    def distance_to(self, position, return_vector=False):
        if return_vector:
            return (position - self.body.position)
        else:
            return (position - self.body.position).length

    def distance_to_sprite(self, sprite, return_vector=False):
        return self.distance_to(sprite.body.position, return_vector)
    

    def point_towards(self, position, offset_degree=0):
        rot_vec = (position - self.body.position).normalized()
        self.body.angle = rot_vec.angle + offset_degree

    def point_towards_sprite(self, sprite, offset_degree=0):
        self.point_towards(sprite.body.position, offset_degree)

    def point_towards_mouse(self, offset_degree=0):
        self.point_towards(pygame.mouse.get_pos(), offset_degree)



    def lock_to(self, sprite, offset):
        assert self.body.body_type == pymunk.Body.KINEMATIC, "only KINEMATIC object can be locked to another sprite"
        
        self.lock_to_sprite = sprite
        self.lock_offset = offset

    def release_position_lock(self):
        self.lock_to_sprite = None
        self.lock_offset = None
        pass

    def set_rotation_style_all_around(self):
        self.rotation_style = RotationStyle.ALL_AROUND

    def set_rotation_style_left_right(self):
        self.rotation_style = RotationStyle.LEFTRIGHT

    def set_rotation_style_no_rotation(self):
        self.rotation_style = RotationStyle.FIXED


    def clone_myself(self):

        sprite = type(self)(
            frame_dict = self.frame_dict_original, 
            starting_mode = self.frame_mode, 
            pos = (self.x, self.y),
            shape_type = self.shape_type, 
            shape_factor = self.shape_factor, 
            body_type = self.body.body_type, 
        )
        if not self in game.all_sprites_to_show:
            game.hide_sprite(sprite)
        sprite.set_rotation(self.get_rotation())
        sprite.scale_by(self.scale_factor)
        sprite.set_frame(self.frame_idx)
        sprite.set_draggable(self.draggable)
        sprite.set_elasticity(self.elasticity)
        sprite.set_friction(self.friction)
        sprite.rotation_style = self.rotation_style


        game.clone_event_manager.on_clone(self, sprite)
        return sprite
    


    # alias of pygame method
    def when_started_as_clone(self, associated_sprites: Iterable[ScratchSprite]=[]):
        
        return game.when_started_as_clone(self, associated_sprites)    


    ## scratch events

    def when_game_start(self, other_associated_sprites: Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_game_start(associated_sprites)
            
    def when_key_pressed(self, key, other_associated_sprites: Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_key_pressed(key, associated_sprites)
    
    def when_any_key_pressed(self, other_associated_sprites: Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_any_key_pressed(associated_sprites)
    
    def when_this_sprite_clicked(self, other_associated_sprites: Iterable[ScratchSprite]=[]):
        return game.when_this_sprite_clicked(self, other_associated_sprites)
       
    def when_backdrop_switched(self, idx, other_associated_sprites : Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_backdrop_switched(idx, associated_sprites)
    
    def when_any_backdrop_switched(self, other_associated_sprites : Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_any_backdrop_switched(associated_sprites)

    def when_timer_above(self, t, other_associated_sprites : Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_timer_above(t, associated_sprites)
    
    def when_receive_message(self, topic: str, other_associated_sprites : Iterable[ScratchSprite]=[]):
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_receive_message(topic, associated_sprites)
    

    def broadcast_message(self, topic: str, data: Any):
        """completely unnecessary"""
        return game.broadcast_message(topic, data)
    

    ## additional events
    def when_condition_met(self, checker=lambda: False, repeats=np.inf, other_associated_sprites: Iterable[ScratchSprite]=[]):
           
        associated_sprites = list(other_associated_sprites) + [self]

        return game.when_condition_met(checker, repeats, associated_sprites)
    
    
    def when_timer_reset(self, reset_period=np.inf, repeats=np.inf, other_associated_sprites: Iterable[ScratchSprite]=[]):
        
        associated_sprites = list(other_associated_sprites) + [self]

        return game.when_timer_reset(reset_period, repeats, associated_sprites)
    
    
    def create_specific_collision_trigger(self, other_sprite: ScratchSprite, other_associated_sprites: Iterable[ScratchSprite]=[]):
        return game.create_specific_collision_trigger(self, other_sprite, other_associated_sprites)
    

    def is_touching(self, other_sprite):
        return sensing.is_touching(self, other_sprite)
    
    def is_touching_mouse(self):
        return sensing.is_touching_mouse(self)
    
    def hide(self):
        game.hide_sprite(self)

    def show(self):
        game.show_sprite(self)

    @override
    def remove(self, *_):
        game.remove_sprite(self)
