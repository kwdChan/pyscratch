from typing import Any, Dict, Hashable, List, Optional, cast
import pygame 
import pymunk
from .helper import adjust_brightness, set_transparency
def circle_sprite(colour, radius, *args, **kwargs):
    circle = create_circle(colour, radius)
    return ScratchSprite({"always":[circle]}, "always", *args, **kwargs)


def rect_sprite(colour, width, height, *args, **kwargs):
    rect = create_rect(colour, width, height)
    return ScratchSprite({"always":[rect]}, "always", *args, **kwargs)


def create_circle(colour, radius):
    surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(surface, colour, (radius, radius), radius)
    return surface


def create_rect(colour, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, colour, surface.get_rect())
    return surface




class ScratchSprite(pygame.sprite.Sprite):
    
    def __init__(self, frame_dict: Dict[Hashable, List[pygame.Surface]], starting_mode, pos, shape_type='box', shape_factor=1, body_type=pymunk.Body.KINEMATIC):
        # DYNAMIC, KINEMATIC, STATIC
        # TODO: add all the properties here

        super().__init__()
        self.frame_dict_original:Dict[Hashable, List[pygame.Surface]] = frame_dict.copy() # never changed
        self.frame_dict:Dict[Hashable, List[pygame.Surface]] = frame_dict.copy() # transformed on the spot

        self.frames: List[pygame.Surface] # updated on the spot
        self.frame_mode: Hashable
        
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

        self.private_data = {}
        self.flip_y = False
        self.flip_x = False
        self.transparency_factor = 1.0
        self.brightness_factor = 1.0

        self.lock_to_sprite = None
        self.lock_offset = 0, 0



    def is_mouse_selected(self):
        return self.mouse_selected
    
    def set_draggable(self, draggable):
        self.draggable = draggable

    def set_is_dragging(self, is_dragging):
        self.is_dragging = is_dragging

    def set_frame_mode(self, new_mode):
        self.frame_mode = new_mode
        self.frames = self.frame_dict[new_mode]

    def flip_horizontal(self):
        self.flip_x = not self.flip_x

    def flip_vertical(self):
        self.flip_y = not self.flip_y

    def update(self, space):

        if self.lock_to_sprite:
            self.body.position = self.lock_to_sprite.body.position + self.lock_offset
            self.body.velocity = 0, 0 

        x, y = self.body.position
        img = self.frames[self.frame_idx]
        img = pygame.transform.flip(img, self.flip_x, self.flip_y)
        img = pygame.transform.rotate(img, -self.body.rotation_vector.angle_degrees)
        self.image = img

        img_w, img_h = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect(
            center=(x, y),
              width=img_w,
              height=img_h,
              )


        if self.new_shape: 
            space.remove(self.shape)
            self.new_shape.collision_type = 1 if self.collision_allowed else 0
            self.shape, self.new_shape = self.new_shape, None
            space.add(self.shape)

        if self.is_dragging:
            self.body.velocity=0,0 
            # TODO: should be done every physics loop or reset location every frame
            # or can i change it to kinamatic temporarily

    def set_mass(self, mass):
        self.body.mass = mass

    def set_moment(self, moment):
        self.body.moment = moment
    
    def set_shape(self, shape_type='box', shape_factor=1.0, collision_allowed=False):
        # could be a function or a string
        # TODO: raise error when invalid mode is selected
        self.shape_type = shape_type
        self.shape_factor = shape_factor
        self.collision_allowed = collision_allowed

        self.request_update_shape()


    def request_update_shape(self):
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
        self.request_update_shape()

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
        self.blit(text_surface)

    def blit(self, surface: pygame.Surface, offset=(0,0)):
        self.frames[self.frame_idx].blit(surface, offset)

    @property
    def direction(self):
        return self.body.rotation_vector.angle_degrees
    
    # the use of setter should discouraged...
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
        self.body.angle = degree/180*3.14159265

    def add_rotation(self, degree):
        self.body.angle += degree/180*3.14159265

    def set_frame(self, idx):
        self.frame_idx = idx
    
    def next_frame(self):
        self.set_frame((self.frame_idx+1) % len(self.frames))


    def move_indir(self, length):
        self.body.position += self.body.rotation_vector*length
        
        

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
    

    
