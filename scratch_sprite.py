import pygame 


class ScratchSprite(pygame.sprite.Sprite):
    def __init__(self, frames, pos):
        # 
        super().__init__()
        self.frames = frames
        self.set_frame(0)

        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)

            
        
    def set_collision_rect(self):
        pass


    def update(self):
        pass

    def set_frame(self, idx):
        self.frame_idx = idx
        self.image = self.frames[self.frame_idx]
    
    def next_frame(self):
        self.set_frame((self.frame_idx+1) % len(self.frames))

    def move_xy(self, xy):
        self.rect.move_ip(xy)

    def move(self, step):
        self.rect



    def show(self):
        pass

