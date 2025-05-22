import pygame 
import pymunk


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
    
    def __init__(self, frame_dict, starting_mode, pos, body_type=pymunk.Body.KINEMATIC):
        # DYNAMIC, KINEMATIC, STATIC
        # TODO: add all the properties here
        super().__init__()
        self.frame_dict = frame_dict
        
        self.set_frame_mode(starting_mode)
        self.set_frame(0)

        self.body = pymunk.Body(1, 100, body_type=body_type)
        self.body.position = pos
        
        
        self.set_shape('box')
        self.shape = None
        self.shape, self.new_shape = self.new_shape, None

    def set_frame_mode(self, new_mode):
        self.frame_mode = new_mode
        self.frames = self.frame_dict[new_mode]

    def update(self, space):
        x, y = self.body.position
        self.image = pygame.transform.rotate(self.frames[self.frame_idx], -self.body.rotation_vector.angle_degrees)
        self.rect = self.image.get_rect(center=(x, y))

        if (not self.shape_type) and (self.shape):
            space.remove(self.shape)
            self.shape = None

        if self.new_shape: 
            space.remove(self.shape)
            self.new_shape.collision_type = self.shape.collision_type
            self.shape, self.new_shape = self.new_shape, None
            space.add(self.shape)
    
    def set_shape(self, shape_type=None, shape_factor=1):
        # could be a function or a string
        # TODO: raise error when invalid mode is selected
        self.shape_type = shape_type
        self.shape_factor = shape_factor
        self.scale(1)

    
    def scale(self, factor):
        # TODO: 
        # use with caution: this creates a new shape for the object
        for k, frames in self.frame_dict.items():
            self.frame_dict[k] = [pygame.transform.scale_by(f, factor) for f in frames]

        self.set_frame_mode(self.frame_mode)

        self.rect = self.frames[self.frame_idx].get_rect()
        self.rect.move_ip(self.body.position)
        

        if self.shape_type == 'box': 
            size = int(self.rect.width*self.shape_factor), int(self.rect.height*self.shape_factor)
            self.new_shape = pymunk.Poly.create_box(self.body, size)
        elif self.shape_type == 'circle':
            radius = (self.shape_factor*(self.rect.width+self.rect.height))//4
            self.new_shape = pymunk.Circle(self.body,radius)
        elif self.shape_type == 'circle_width':
            self.new_shape = pymunk.Circle(self.body, (self.shape_factor*self.rect.width)//2)

        elif self.shape_type == 'circle_height':
            self.new_shape = pymunk.Circle(self.body, (self.shape_factor*self.rect.height)//2)
        elif self.shape_type:
            # self.shape_type is a function that returns the shape
            self.new_shape = self.shape_type(factor, self.shape_factor)
        else: 
            pass

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

    def move_xy(self, xy):
        self.body.position = self.body.position + xy

