import pygame
import pymunk
from event import Event
from scratch_sprite import rect_sprite
from pymunk.pygame_util import DrawOptions


def collision_begin(arbiter, space, data):
    data['self'].contact_pairs_set.add(arbiter.shapes) 
    print(0)

    for e, (a,b) in Event.collision_pairs.items():
        if (a.shape in arbiter.shapes) and (b.shape in arbiter.shapes):
            e.trigger(arbiter)
    return True#False

def collision_separate(arbiter, space, data):
    if arbiter.shapes in data['self'].contact_pairs_set:
        data['self'].contact_pairs_set.remove(arbiter.shapes)

class Game:

    def __init__(self, screen_size=(1280, 720)):

        self.screen  = pygame.display.set_mode(screen_size, vsync=1)
        self.space = pymunk.Space()

        self.contact_pairs_set = set() 

        self.collision_handler = self.space.add_collision_handler(1, 1)
        self.collision_handler.data['self'] =self
        self.collision_handler.begin = collision_begin
        self.collision_handler.separate = collision_separate

        self.draw_options = DrawOptions(self.screen)

        # test only
        self.space.gravity=0,.001
        seg = pymunk.Segment(self.space.static_body, (0, 200), (1000, 1000), 25)
        self.space.add(seg)
        self.seg = seg
        # test only --end
    
        self.all_sprites = pygame.sprite.Group()

        self.data = {}

        # edges
        edge_colour = (255, 0, 0)
        edge_body = pymunk.Body.KINEMATIC
        screen_w, screen_h = screen_size


        top_edge = rect_sprite(edge_colour, screen_w, 4, (screen_w//2, 0),body_type= edge_body)
        bottom_edge = rect_sprite(edge_colour, screen_w, 4, (screen_w//2, screen_h),body_type= edge_body)
        left_edge = rect_sprite(edge_colour, 4, screen_h, (0, screen_h//2),body_type= edge_body)
        right_edge = rect_sprite(edge_colour, 4, screen_h, (screen_w,  screen_h//2),body_type= edge_body)

        self.add_sprite(top_edge)
        self.add_sprite(bottom_edge)
        self.add_sprite(left_edge)
        self.add_sprite(right_edge)
        

    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)

    def start(self, framerate, sim_step_min=300, debug_draw=True):


        clock = pygame.time.Clock()

        draw_every_n_step = sim_step_min//framerate
        frame_count = 0
        while True:
            frame_count += 1

            # TODO: there is no need to wait between each simulation step. 
            # all the simulation steps between the frames can be run instantly 
            dt = clock.tick(framerate*draw_every_n_step)
            self.space.step(dt)

            time = pygame.time.get_ticks()

            for c in Event.timer_event_checkers:
                c(time)

            for c in Event.overlap_event_checkers:
                c()

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

        