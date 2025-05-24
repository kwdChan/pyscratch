import pygame
import pymunk
import numpy as np
class Trigger:
    all_triggers = []
    def __init__(self, condition_checker):
        self.condition_checker = condition_checker
        self.func = lambda: None
        type(self).all_triggers.append(self)
    
    def do(self, func):
        self.func = func
    
    def check(self):
        if self.condition_checker():
            self.func()
            type(self).all_triggers.remove(self)


class Event:
    active_events = []

    def __init__(self, active=True):
        self.triggers = []
        self.handlers = []

        if active: 
            self.active()

    def inactive(self):
        type(self).active_events.remove(self)

    def active(self):
        assert not (self in type(self).active_events)
        type(self).active_events.append(self)


    def trigger(self, *args, **kwargs):
        self.triggers.append((args, kwargs))
    
    def add_handler(self, func):
        self.handlers.append(func)

    def handle_all(self):
        while self.handle_one():
            pass
        

    def handle_one(self):
        if not len(self.triggers): 
            return False
        
        args, kwargs = self.triggers.pop(0)

        for h in self.handlers:
            h(*args, **kwargs)

        return True
    
    timer_event_checkers = []
    def create_timer_event(period_sec, n_times=np.inf):
        event = Event()
        
        period_ms = period_sec*1000
        time_ms_last = 0

        counter = 0

        def check_trigger(time_ms_new):
            nonlocal time_ms_last, counter

            dt = time_ms_new - time_ms_last
            if dt >= period_ms:
                event.trigger()
                time_ms_last = time_ms_new
                counter += 1
                #print(dt)
                if counter >= n_times:
                    # remove itself from the active event list
                    # TODO: unclear if the object is completely dereferenced
                    event.add_handler(lambda: event.inactive())
                    Event.timer_event_checkers.remove(check_trigger)

        Event.timer_event_checkers.append(check_trigger)

        return event#, check_trigger
    

    
    
    pygame_event_checkers = []


    def create_pygame_event(flags):
        event = Event()

        def check_trigger(pygame_event_list):
            for pygame_event in pygame_event_list:
                if pygame_event.type in flags:
                    event.trigger(pygame_event)

        Event.pygame_event_checkers.append(check_trigger)
        return event
    
    subscriptions = {} 

    def new_subscription(topic, event):
        if not (topic in Event.subscriptions):
            Event.subscriptions[topic] = []

        Event.subscriptions[topic].append(event)
        

    def create_messager_event(topic):
        event = Event()
        Event.new_subscription(topic, event)
        return event
    

    def submit_message(topic, *arg, **kwargs):
        if not topic in Event.subscriptions:
            return 
        
        for e in Event.subscriptions[topic]:
            e.trigger(*arg, **kwargs)

    overlap_event_checkers = []
    # def create_overlap_event(sprite_a, sprite_b, rect_or_circle='rect'):
    #     event = Event()
        
    #     if rect_or_circle == 'rect':
    #         detection_func = pygame.sprite.collide_rect
    #     elif rect_or_circle == 'circle':
    #         detection_func = pygame.sprite.collide_circle

    #     def checker():
    #         if detection_func(sprite_a, sprite_b):
    #             event.trigger()

    #     Event.overlap_event_checkers.append(checker)

    #     return event
        

    collision_pairs = {}

    def create_collision_event(sprite_a, sprite_b):
        event = Event()
        sprite_a.shape.collision_type = 1
        sprite_b.shape.collision_type = 1
        Event.collision_pairs[event] = sprite_a, sprite_b

        return event

        
        