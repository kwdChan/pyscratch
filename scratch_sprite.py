import pygame 
import pymunk
from event import Event
from helper import adjust_brightness
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
    
    def __init__(self, frame_dict, starting_mode, pos, shape_type='box', shape_factor=1, body_type=pymunk.Body.KINEMATIC):
        # DYNAMIC, KINEMATIC, STATIC
        # TODO: add all the properties here
        super().__init__()
        self.frame_dict_original = frame_dict.copy() 
        self.frame_dict = frame_dict.copy()
        
        self.set_frame_mode(starting_mode)
        self.set_frame(0)

        self.body = pymunk.Body(1, 100, body_type=body_type)
        self.body.position = pos
        
        self.scale_factor = 1

        self.set_shape(shape_type, shape_factor)
        self.shape = None
        self.shape, self.new_shape = self.new_shape, None

        self.mouse_selected = False
        self.is_dragging = False
        self.draggable = False

        self.private_data = {}
        self.flip_y = False
        self.flip_x = False

        self.on_mouse_click_event = Event()
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


        if (not self.shape_type) and (self.shape):
            space.remove(self.shape)
            self.shape = None

        if self.new_shape: 
            space.remove(self.shape)
            #self.new_shape.collision_type = self.shape.collision_type
            self.new_shape.collision_type = 0 if self.collision_allowed else 2
            self.shape, self.new_shape = self.new_shape, None
            space.add(self.shape)

        if self.is_dragging:
            self.body.velocity=0,0
    
    def set_shape(self, shape_type='box', shape_factor=1, collision_allowed=False):
        # could be a function or a string
        # TODO: raise error when invalid mode is selected
        self.shape_type = shape_type
        self.shape_factor = shape_factor
        self.collision_allowed= collision_allowed
        self.scale_by(1)


    def set_scale(self, factor):
        self.scale_factor = factor
        self.scale_by(1)
    

    
    def scale_by(self, factor):


        new_factor = self.scale_factor*factor
        self.scale_factor = new_factor

        # TODO: 
        # use with caution: this creates a new shape for the object
        for k, frames in self.frame_dict_original.items():
            self.frame_dict[k] = [pygame.transform.scale_by(f, new_factor) for f in frames]

        self.set_frame_mode(self.frame_mode)

        # the rect here has no effect
        self.rect = self.frames[self.frame_idx].get_rect()
        self.rect.width = int(self.rect.width*self.shape_factor)
        self.rect.height = int(self.rect.height*self.shape_factor)
        #self.rect.move_ip(self.body.position)
        

        if self.shape_type == 'box': 
            size = int(self.rect.width), int(self.rect.height)
            self.new_shape = pymunk.Poly.create_box(self.body, size)
        elif self.shape_type == 'circle':
            radius = ((self.rect.width+self.rect.height))//4
            self.new_shape = pymunk.Circle(self.body,radius)
        elif self.shape_type == 'circle_width':
            self.new_shape = pymunk.Circle(self.body, (self.rect.width)//2)

        elif self.shape_type == 'circle_height':
            self.new_shape = pymunk.Circle(self.body, (self.rect.height)//2)

        elif self.shape_type:
            # in this case, self.shape_type is a function that returns the shape

            # factor is the change_factor, new_factor is the overall factor
            self.new_shape = self.shape_type(new_factor, factor, self.shape_factor)
        else: 
            pass

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
    def y(self):
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
    
    def point_towards_mouse(self, sprite, return_vector=False):
        return self.distance_to(pygame.mouse.get_pos(), return_vector)


    def point_towards(self, position, offset_degree=0):
        rot_vec = (position - self.body.position).normalized()
        self.body.angle = rot_vec.angle + offset_degree

    def point_towards_sprite(self, sprite, offset_degree=0):
        self.point_towards(sprite.body.position, offset_degree)

    def point_towards_mouse(self, offset_degree=0):
        self.point_towards(pygame.mouse.get_pos(), offset_degree)


    def change_brightness(self, factor):
        # for k, frames in self.frame_dict_original.items():
        #     self.frame_dict[k] = [adjust_brightness(f, factor) for f in frames]

        # self.set_frame_mode(self.frame_mode)
        pass
    


    def change_transparency(self):
        pass


    def lock_to(self, sprite, offset):
        assert self.body.body_type == pymunk.Body.KINEMATIC, "only KINEMATIC object can be locked to another sprite"
        
        self.lock_to_sprite = sprite
        self.lock_offset = offset

    def release_position_lock(self):
        self.lock_to_sprite = None
        self.lock_offset = None
        pass
    

    
