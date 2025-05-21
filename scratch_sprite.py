import pygame 
import pymunk

class ScratchSprite(pygame.sprite.Sprite):
    
    def __init__(self, frames, pos, body_type=pymunk.Body.KINEMATIC):
        # DYNAMIC, KINEMATIC, STATIC
        super().__init__()
        self.frames = frames
        self.set_frame(0)

        self.body = pymunk.Body(1, 1, body_type=body_type)
        self.body.position = pos
        
        self.scale(1)
        self.shape, self.new_shape = self.new_shape, None

    def update(self, space):
        x, y = self.body.position
        self.image = pygame.transform.rotate(self.frames[self.frame_idx], -self.body.rotation_vector.angle_degrees)
        self.rect = self.image.get_rect(center=(x, y))

        if self.new_shape: 
            space.remove(self.shape)
            self.shape, self.new_shape = self.new_shape, None
            space.add(self.shape)
    
    def scale(self, factor):
        # use with caution: this creates a new shape for the object
        self.frames = [pygame.transform.scale_by(f, factor) for f in self.frames]

        self.rect = self.frames[self.frame_idx].get_rect()
        self.rect.move_ip(self.body.position)
        
        size = self.rect.width, self.rect.height
        self.new_shape = pymunk.Poly.create_box(self.body, size)

    def get_rotation(self):
        return self.body.rotation_vector.angle_degrees

    def set_frame(self, idx):
        self.frame_idx = idx
        #self.image = self.frames[self.frame_idx]
    
    def next_frame(self):
        self.set_frame((self.frame_idx+1) % len(self.frames))

    def move_xy(self, xy):
        self.body.position = self.body.position + xy

