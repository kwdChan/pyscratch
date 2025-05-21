import pygame
import pymunk
from event import Event

from pymunk.pygame_util import DrawOptions
class Game:
    def __init__(self, screen_size=(1280, 720)):
        self.screen  = pygame.display.set_mode(screen_size, vsync=1)
        self.space = pymunk.Space()

        self.draw_options = DrawOptions(self.screen)

        # test only
        self.space.gravity=0,.0001
        seg = pymunk.Segment(self.space.static_body, (0, 200), (1000, 1000), 25)
        self.space.add(seg)
        self.seg = seg
        # test only --end
    
        self.all_sprites = pygame.sprite.Group()

        self.data = {}

    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)

    def start(self, framerate, sim_step_min=300, debug_draw=True):


        clock = pygame.time.Clock()

        draw_every_n_step = sim_step_min//framerate
        frame_count = 0
        while True:
            frame_count += 1
 
            dt = clock.tick(framerate*draw_every_n_step)
            self.space.step(dt)

            time = pygame.time.get_ticks()

            for c in Event.timer_event_checkers:
                c(time)

            all_events = pygame.event.get()

            for event in all_events:
                if event.type == pygame.QUIT:
                    pygame.quit()

            for c in Event.pygame_event_checkers:
                c(all_events)


            # execute 
            for e in Event.active_events:
                e.handle_all()

            if not frame_count % draw_every_n_step: 
                frame_count = 0
                self.screen.fill((30, 30, 30))

                self.all_sprites.update(self.space)
                self.all_sprites.draw(self.screen)

                if debug_draw: 
                    self.space.debug_draw(self.draw_options)
                
                pygame.display.flip()

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)
        self.space.add(sprite.body, sprite.shape)

game = Game()

        