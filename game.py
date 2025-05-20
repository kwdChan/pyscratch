import pygame
from event import Event

class Game:
    def __init__(self, screen_size=(1280, 720)):
        self.screen  = pygame.display.set_mode(screen_size)

        self.all_sprites = pygame.sprite.Group()

        self.data = {}

    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)

    def start(self, framerate):


        clock = pygame.time.Clock()


        while True:

            
            dt = clock.tick(framerate)

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

            

            # all_sprites.update(dt)
            self.screen.fill((30, 30, 30))

            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)

game = Game()

        