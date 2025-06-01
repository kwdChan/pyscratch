import numpy as np
import pygame
import pymunk
from .event import ConditionInterface, Trigger, Condition, TimerCondition
from .scratch_sprite import rect_sprite, ScratchSprite
from pymunk.pygame_util import DrawOptions
from typing import Any, Callable, Optional, List, Dict, Set, Tuple, cast




def collision_begin(arbiter, space, data):
    game = cast(Game, data['game'])
    game.contact_pairs_set.add(arbiter.shapes) 

    for e, (a,b) in game.trigger_to_collision_pairs.items():
        if (a.shape in arbiter.shapes) and (b.shape in arbiter.shapes):
            e.trigger(arbiter)


    colliding_types = arbiter.shapes[0].collision_type, arbiter.shapes[1].collision_type
    collision_allowed = True
    for collision_type, (allowed, triggers) in game.collision_type_to_trigger.items():
        if collision_type in colliding_types: 
            [t.trigger(arbiter) for t in triggers]
            collision_allowed = collision_allowed and allowed
        

    if (arbiter.shapes[0].collision_type == 0) or (arbiter.shapes[1].collision_type == 0):
        collision_allowed = False


    return collision_allowed

def collision_separate(arbiter, space, data):
    game = cast(Game, data['game'])
    if arbiter.shapes in game.contact_pairs_set:
        game.contact_pairs_set.remove(arbiter.shapes)

class Game:

    def __init__(self, screen_size=(1280, 720)):
        pygame.init()

        self.screen  = pygame.display.set_mode(screen_size, vsync=1)
        self.space = pymunk.Space()
        self.draw_options = DrawOptions(self.screen)

        # sounds
        self.mixer = pygame.mixer.init()
        self.sounds = {}

        # shared variables 
        self.shared_data = {}
        
        # collision detection
        self.trigger_to_collision_pairs = {}
        self.collision_type_pair_to_trigger: Dict[Tuple[int, int], List[Trigger]] = {}
        self.collision_type_to_trigger: Dict[int, Tuple[bool, List[Trigger]]] = {}

        self.contact_pairs_set: Set[pymunk.Shape] = set() 
        self.collision_handler = self.space.add_default_collision_handler()
        self.collision_handler.data['game'] = self
        self.collision_handler.begin = collision_begin
        self.collision_handler.separate = collision_separate
        
        # sprites updating and drawing
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_to_show = pygame.sprite.LayeredUpdates()


        # # scheduled jobs
        # self.pre_scheduled_jobs = []
        # self.scheduled_jobs = []


        self.all_pygame_events = []
        self.all_triggers: List[Trigger] = [] # these are to be executed every iteration
        self.all_conditions: List[ConditionInterface] = [] # these are to be checked every iteration
        #self.all_forever_jobs: List[Callable[[], None]] = []
        self.all_message_subscriptions: Dict[str, List[Trigger]] = {}
        
        # key events 
        key_event = self.create_pygame_event_trigger([pygame.KEYDOWN, pygame.KEYUP])
        key_event.add_callback(self.__key_event_handler)
        self.all_simple_key_triggers: List[Trigger] = [] # these are to be triggered by self.__key_event_handler only

        # mouse dragging event
        self.dragged_sprite = None
        self.drag_offset = 0, 0
        self.sprite_click_trigger:Dict[ScratchSprite, Trigger] = {}  #TODO: need to be able to destory the trigger here when the sprite is destoryed
        mouse_drag_trigger = self.create_pygame_event_trigger([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        mouse_drag_trigger.add_callback(self.__mouse_drag_handler)

        ## Backdrops
        self.backdrops = []
        self.__backdrop_index = None
        self.backdrop_change_trigger = self.create_trigger()


    def __key_event_handler(self, e):
        up_or_down = 'down' if e.type == pygame.KEYDOWN else 'up'
        keyname = pygame.key.name(e.key)

        for t in self.all_simple_key_triggers:
            t.trigger(keyname, up_or_down)

    def create_key_trigger(self):
        t = self.create_trigger()
        self.all_simple_key_triggers.append(t)
        return t


    def __mouse_drag_handler(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN: 
            
            for s in reversed(list(self.all_sprites_to_show)):
                s = cast(ScratchSprite, s)

                if s.shape.point_query(e.pos).distance <= 0:
                    self.sprite_click_trigger[s].trigger()

                    if not s.draggable:
                        continue

                    s.set_is_dragging (True)
                    self.dragged_sprite = s
                    offset_x = s.body.position[0]  - e.pos[0]
                    offset_y = s.body.position[1]  - e.pos[1]
                    self.drag_offset = offset_x, offset_y
                    break 

        elif e.type == pygame.MOUSEBUTTONUP:
            if self.dragged_sprite: 
                self.dragged_sprite.set_is_dragging(False)
                self.dragged_sprite = None

        elif e.type == pygame.MOUSEMOTION and self.dragged_sprite:
            x = e.pos[0] + self.drag_offset[0]
            y = e.pos[1] + self.drag_offset[1]
            self.dragged_sprite.set_xy((x,y))


    def create_edges(self, edge_colour = (255, 0, 0), thickness=4):
        # edges
        edge_body = pymunk.Body.STATIC
        screen_w, screen_h = self.screen.get_width(), self.screen.get_height()

        top_edge = rect_sprite(edge_colour, screen_w, thickness, (screen_w//2, 0),body_type= edge_body)
        bottom_edge = rect_sprite(edge_colour, screen_w, thickness, (screen_w//2, screen_h),body_type= edge_body)
        left_edge = rect_sprite(edge_colour, thickness, screen_h, (0, screen_h//2),body_type= edge_body)
        right_edge = rect_sprite(edge_colour, thickness, screen_h, (screen_w,  screen_h//2),body_type= edge_body)

        top_edge.set_collision_type(1)
        bottom_edge.set_collision_type(1)
        left_edge.set_collision_type(1)
        right_edge.set_collision_type(1)


        self.add_sprite(top_edge)
        self.add_sprite(bottom_edge)
        self.add_sprite(left_edge)
        self.add_sprite(right_edge)

        self.shared_data['top_edge'] = top_edge
        self.shared_data['left_edge'] = left_edge
        self.shared_data['bottom_edge'] = bottom_edge
        self.shared_data['right_edge'] = right_edge

        return top_edge, left_edge, bottom_edge, right_edge

    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)

    # def schedule_job(self, delay, func):
    #     self.pre_scheduled_jobs.append((delay*1000, func))

    # def __schedule_jobs(self, time):
    #     for delay, func in self.pre_scheduled_jobs:
    #         self.scheduled_jobs.append((time+delay, func))
    #     self.pre_scheduled_jobs = []

    # def __run_jobs(self, time):
    #     i = len(self.scheduled_jobs)
    #     while i:
    #         due_time, func = self.scheduled_jobs[i-1]
    #         if due_time < time:
    #             func()  
    #             self.scheduled_jobs.pop(i-1)
    #         i-=1


    def create_pygame_event_trigger(self, flags: List[int]):

        condition = self.create_conditional_trigger()
        
        def checker_hijack():
            for e in self.all_pygame_events:
                if e.type in flags:
                    condition.trigger.trigger(e)

            if not condition.trigger.stay_active:
                condition.remove()

        condition.change_checker(checker_hijack)
        return condition.trigger


    def create_timer_trigger(self, reset_period=np.inf, repeats=np.inf):
        condition = TimerCondition(reset_period,repeats)
        self.all_conditions.append(condition)
        self.all_triggers.append(condition.trigger)
        return condition

    def create_specific_collision_trigger(self, sprite1: ScratchSprite, sprite2: ScratchSprite):

        #"""Cannot change the collision type of the obbject after calling this function"""
        trigger = self.create_trigger()

        self.trigger_to_collision_pairs[trigger] = sprite1, sprite2

        return trigger

    def create_type2type_collision_trigger(self, type_a, type_b, collision_suppressed=False):
        pair = (type_a, type_b) if type_a>type_b else (type_b, type_a)

        h = self.space.add_collision_handler(*pair)
        trigger = self.create_trigger()
        
        if not pair in self.collision_type_pair_to_trigger: 
            self.collision_type_pair_to_trigger[pair] = []
        self.collision_type_pair_to_trigger[pair].append(trigger)

        collision_allowed = not collision_suppressed
        def begin(arbiter, space, data):
            game = cast(Game, data['game'])
            game.contact_pairs_set.add(arbiter.shapes) 

            for t in game.collision_type_pair_to_trigger[pair]:
                t.trigger(arbiter)
            return collision_allowed
        
        h.data['game'] = self
        h.begin = begin
        h.separate = collision_separate
        
        return trigger


    def create_type_collision_trigger(self, collision_type, collision_suppressed=False):
        trigger = self.create_trigger()

        collision_allowed = not collision_suppressed
        

        if not collision_type in self.collision_type_to_trigger: 
            self.collision_type_to_trigger[collision_type] = collision_allowed, []


        self.collision_type_to_trigger[collision_type][1].append(trigger)

        
    
        return trigger
    
    def suppress_type_collision(self, collision_type, collision_suppressed=True):
        collision_allowed = not collision_suppressed

        if not collision_type in self.collision_type_to_trigger: 
            self.collision_type_to_trigger[collision_type] = collision_allowed, []    
        else:
            t_list = self.collision_type_to_trigger[collision_type][1]
            self.collision_type_to_trigger[collision_type] = collision_allowed, t_list



    def retrieve_sprite_click_trigger(self, sprite):
        return self.sprite_click_trigger[sprite]
        
    def new_subscription(self, topic: str, trigger: Trigger):
        if not (topic in self.all_message_subscriptions):
            self.all_message_subscriptions[topic] = []

        self.all_message_subscriptions[topic].append(trigger)

        
    def create_messager_trigger(self, topic: str):
        trigger = self.create_trigger()
        self.new_subscription(topic, trigger)
        return trigger
    
    def boardcast_message(self, topic: str, data: Any):
        if not topic in self.all_message_subscriptions:
            return 
        
        self.all_message_subscriptions[topic] = list(filter(lambda t: t.stay_active, self.all_message_subscriptions[topic]))
        for e in self.all_message_subscriptions[topic]:

            e.trigger(data)
            

    def create_conditional_trigger(self, checker=lambda: False, repeats=np.inf):
        condition = Condition(checker, repeats)
        self.all_conditions.append(condition)
        self.all_triggers.append(condition.trigger)
        return condition
    
    def create_trigger(self):
        trigger = Trigger()
        self.all_triggers.append(trigger)
        return trigger
    
    # # not sure if this should be exposed
    # def __run_forever(self, func: Callable[[], None]):
    #     self.all_forever_jobs.append(func)


    def load_sound(self, key, path) :
        if key in self.sounds: 
            raise KeyError(f'{key} already loaded. Choose a different key name.')
        
        self.sounds[key] = pygame.mixer.Sound(path)

    def play_sound(self, key, volume=1.0):
        s = self.sounds[key]
        s.set_volume(volume)
        s.play()
    

    def start(self, framerate, sim_step_min=300, debug_draw=False, event_count=False):


        clock = pygame.time.Clock()

        draw_every_n_step = sim_step_min//(framerate*2)+1

        current_time = 0

        draw = True
        while True:
            dt = clock.tick(framerate*2)
            current_time += dt
            for i in range(draw_every_n_step): 
                self.space.step(dt/draw_every_n_step)


            #all_events = pygame.event.get()

            self.all_pygame_events = pygame.event.get()
            # TODO: refactor
            for event in self.all_pygame_events:
                if event.type == pygame.QUIT:
                    #pygame.quit()
                    return 


            # for j in self.all_forever_jobs:
            #     j()

            # check conditions
            if draw:
                for c in self.all_conditions:
                    c.check()

                # execute 
                for t in self.all_triggers:
                    t.handle_all(current_time)
                    # TODO: is it possible to remove t in the self.all_triggers here?
                    t.generators_proceed(current_time)

                # clean up
                self.all_conditions = list(filter(lambda t: t.stay_active, self.all_conditions))
                self.all_simple_key_triggers = list(filter(lambda t: t.stay_active, self.all_simple_key_triggers))
                self.all_triggers = list(filter(lambda t: t.stay_active, self.all_triggers))

                
                if event_count: 
                    print("all_conditions", len(self.all_conditions))
                    print("all_triggers", len(self.all_triggers))
                    print("all sprite", len(self.all_sprites))
                    # print("all_simple_key_triggers", len(self.all_simple_key_triggers))

            # Drawing

            if draw: 
                self.screen.fill((30, 30, 30))
                if not (self.__backdrop_index is None): 
                    self.screen.blit(self.backdrops[self.__backdrop_index], (0, 0))

                if debug_draw: 
                    self.space.debug_draw(self.draw_options)
                
                self.all_sprites.update(self.space)
                self.all_sprites_to_show.draw(self.screen)
                pygame.display.flip()
            
            draw = not draw

    def set_gravity(self, xy):
        self.space.gravity = xy

    def add_sprite(self, sprite, to_show=True):
        self.all_sprites.add(sprite)
        self.space.add(sprite.body, sprite.shape)
        if to_show:
            self.all_sprites_to_show.add(sprite)

        self.sprite_click_trigger[sprite] = self.create_trigger()

    def remove_sprite(self, sprite):

        self.all_sprites.remove(sprite)
        self.all_sprites_to_show.remove(sprite) 
        self.sprite_click_trigger[sprite].remove()

        self.trigger_to_collision_pairs = {k: v for k, v in self.trigger_to_collision_pairs.items() if not sprite in v}

        try: 
            self.space.remove(sprite.body, sprite.shape)
        except:
            print('removing non-existing shape or body')


    def show_sprite(self, sprite):
        self.all_sprites_to_show.add(sprite)

    def hide_sprite(self, sprite):
        self.all_sprites_to_show.remove(sprite)

    def bring_to_front(self, sprite):
        self.all_sprites_to_show.move_to_front(sprite)

    def move_to_back(self, sprite):
        self.all_sprites_to_show.move_to_back(sprite)

    def change_layer(self, sprite, layer):
        self.all_sprites_to_show.change_layer(sprite, layer)


    def change_layer_by(self, sprite, by):
        layer = self.all_sprites_to_show.get_layer_of_sprite(sprite)
        self.all_sprites_to_show.change_layer(sprite, layer + by)

    def get_layer_of_sprite(self, sprite):
        self.all_sprites_to_show.get_layer_of_sprite(sprite)

    def set_backdrops(self, images: List[pygame.Surface]):
        self.backdrops = images
    
    @property
    def backdrop_index(self):
        return self.__backdrop_index

    def switch_backdrop(self, index:Optional[int]=None):

        if index != self.__backdrop_index:
            self.__backdrop_index = index
            self.backdrop_change_trigger.trigger(index)

    def next_backdrop(self):
        if not self.__backdrop_index is None: 
            self.switch_backdrop((self.__backdrop_index+1) % len(self.backdrops))
        


    
        
        
game = Game()

        