import pygame
import pymunk
from event import Event

from pymunk.pygame_util import DrawOptions
class Game:
    def __init__(self, screen_size=(1280, 720)):
        self.screen  = pygame.display.set_mode(screen_size, vsync=1)
        self.space = pymunk.Space()
        self.space.gravity=0,.0001

        seg = pymunk.Segment(self.space.static_body, (0, 200), (1000, 1000), 25)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.space.add(seg)
        self.seg = seg
       
        self.all_sprites = pygame.sprite.Group()

        self.data = {}

    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)

    def start(self, framerate):


        clock = pygame.time.Clock()

        stim_factor = 5
        count = 0
        while True:
            count += 1
 
            dt = clock.tick(framerate*stim_factor)
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

            if not count % stim_factor: 
                self.screen.fill((30, 30, 30))

                self.all_sprites.update(self.space)
                self.all_sprites.draw(self.screen)


                self.space.debug_draw(self.draw_options)
                pygame.display.flip()

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)
        self.space.add(sprite.body, sprite.shape)

game = Game()

        