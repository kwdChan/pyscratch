from __future__ import annotations

import numpy as np
import pygame
import pymunk
from .event import ConditionInterface, Trigger, Condition, TimerCondition
from pymunk.pygame_util import DrawOptions
from typing import Any, Callable, Iterable, Optional, List, Dict, Set, Tuple, Union, cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scratch_sprite import ScratchSprite



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


    reverse_order = arbiter.shapes[1], arbiter.shapes[0]
    if reverse_order in game.contact_pairs_set:
        game.contact_pairs_set.remove(reverse_order)



class SpriteEventDependencyManager:
    def __init__(self):

        self.sprites: Dict[ScratchSprite, List[Union[Trigger, ConditionInterface]]] = {}

    def add_event(self, event: Union[ConditionInterface, Trigger], sprites: Iterable[ScratchSprite]):
        """
        TODO: if the event is dependent to multiple sprites, the event will not be
        completely dereferenced until all the sprites on which it depends are removed

        """
        for s in sprites:
            if not s in self.sprites:
                self.sprites[s] = []
            self.sprites[s].append(event)


    def sprite_removal(self, sprite: ScratchSprite):
        
        to_remove = self.sprites.get(sprite)
        if not to_remove:
            return 
    
        for e in to_remove:
            e.remove()
            
class Game:
    singleton_lock = False
    def __init__(self, screen_size=(1280, 720)):
        pygame.init()

        assert not Game.singleton_lock, "Already instantiated."
        Game.singleton_lock = True

        self.screen  = pygame.display.set_mode(screen_size, vsync=1)
        self.space = pymunk.Space()
        self.draw_options = DrawOptions(self.screen)

        # sounds
        self.mixer = pygame.mixer.init()
        self.sounds = {}

        # shared variables 
        self.shared_data = {}
        
        # sprite event dependency manager
        self.sprite_event_dependency_manager = SpriteEventDependencyManager()

        # collision detection
        self.trigger_to_collision_pairs = {}
        self.collision_type_pair_to_trigger: Dict[Tuple[int, int], List[Trigger]] = {}
        self.collision_type_to_trigger: Dict[int, Tuple[bool, List[Trigger]]] = {}

        self.contact_pairs_set: Set[Tuple[pymunk.Shape, pymunk.Shape]] = set() 
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

        self.sprite_click_trigger:Dict[ScratchSprite, List[Trigger]] = {}  #TODO: need to be able to destory the trigger here when the sprite is destoryed
        mouse_drag_trigger = self.create_pygame_event_trigger([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        mouse_drag_trigger.add_callback(self.__mouse_drag_handler)

        ## Backdrops
        self.backdrops = []
        self.__backdrop_index = None
        self.backdrop_change_triggers: List[Trigger] = []


        ## start event
        self.game_start_triggers: List[Trigger] = []

        ## global timer event
        self.global_timer_triggers: List[Trigger] = []

    
        self.current_time: float = 0
        


    def __key_event_handler(self, e):
        up_or_down = 'down' if e.type == pygame.KEYDOWN else 'up'
        keyname = pygame.key.name(e.key)

        for t in self.all_simple_key_triggers:
            t.trigger(keyname, up_or_down)


    def __mouse_drag_handler(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN: 
            
            for s in reversed(list(self.all_sprites_to_show)):
                if TYPE_CHECKING:
                    s = cast(ScratchSprite, s)

                if s.shape.point_query(e.pos).distance <= 0:
                    for t in self.sprite_click_trigger[s]:
                        t.trigger()

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



    def update_screen_mode(self, *arg, **kwargs):
        self.screen  = pygame.display.set_mode( *arg, **kwargs)



    # all events 

    ## scratch events

    def when_game_start(self, associated_sprites : Iterable[ScratchSprite]=[]):
        t = self.create_trigger(associated_sprites)
        self.game_start_triggers.append(t)
        return t
            
    
    def when_key_pressed(self, associated_sprites : Iterable[ScratchSprite]=[]):
        """different to scratch: catch all keys and catch both press and release """
        t = self.create_trigger(associated_sprites)
        self.all_simple_key_triggers.append(t)
        return t
    
    def when_this_sprite_clicked(self, sprite, other_associated_sprites: Iterable[ScratchSprite]=[]):
        t = self.create_trigger(set(list(other_associated_sprites)+[sprite]))

        if not sprite in self.sprite_click_trigger:
            self.sprite_click_trigger[sprite] = []
            
        self.sprite_click_trigger[sprite].append(t)

        return t
        
 
    def when_backdrop_switched(self, associated_sprites : Iterable[ScratchSprite]=[]):
        """different to scratch: catch all switches"""
        t = self.create_trigger(associated_sprites)
        self.backdrop_change_triggers.append(t)
        return t

    def when_timer_above(self, t, associated_sprites : Iterable[ScratchSprite]=[]):
        return self.when_condition_met(lambda:(self.current_time>t), 1, associated_sprites)
   
    def when_receive_message(self, topic: str, associated_sprites : Iterable[ScratchSprite]=[]):
        trigger = self.create_trigger(associated_sprites)
        self.__new_subscription(topic, trigger)
        return trigger
    
    def boardcast_message(self, topic: str, data: Any):
        if not topic in self.all_message_subscriptions:
            return 
        
        self.all_message_subscriptions[topic] = list(filter(lambda t: t.stay_active, self.all_message_subscriptions[topic]))
        for e in self.all_message_subscriptions[topic]:
            e.trigger(data)

    def __new_subscription(self, topic: str, trigger: Trigger):
        if not (topic in self.all_message_subscriptions):
            self.all_message_subscriptions[topic] = []

        self.all_message_subscriptions[topic].append(trigger)



    ## advance events
    def create_pygame_event_trigger(self, flags: List[int], associated_sprites : Iterable[ScratchSprite]=[]):

        condition = self.when_condition_met(associated_sprites)
        
        def checker_hijack():
            for e in self.all_pygame_events:
                if e.type in flags:
                    condition.trigger.trigger(e)

            if not condition.trigger.stay_active:
                condition.remove()

        condition.change_checker(checker_hijack)
        return condition.trigger


    def create_specific_collision_trigger(self, sprite1: ScratchSprite, sprite2: ScratchSprite, other_associated_sprites: Iterable[ScratchSprite]=[]):

        #"""Cannot change the collision type of the object after calling this function"""
        trigger = self.create_trigger(set(list(other_associated_sprites)+[sprite1, sprite2]))

        self.trigger_to_collision_pairs[trigger] = sprite1, sprite2

     
        return trigger

    def create_type2type_collision_trigger(self, type_a, type_b, collision_suppressed=False, associated_sprites: Iterable[ScratchSprite]=[]):
        pair = (type_a, type_b) if type_a>type_b else (type_b, type_a)

        h = self.space.add_collision_handler(*pair)
        trigger = self.create_trigger(associated_sprites)



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


    def create_type_collision_trigger(self, collision_type, collision_suppressed=False, associated_sprites: Iterable[ScratchSprite]=[]):
        trigger = self.create_trigger(associated_sprites)

        collision_allowed = not collision_suppressed
        

        if not collision_type in self.collision_type_to_trigger: 
            self.collision_type_to_trigger[collision_type] = collision_allowed, []


        self.collision_type_to_trigger[collision_type][1].append(trigger)

        return trigger
    

    def when_timer_reset(self, reset_period=np.inf, repeats=np.inf, associated_sprites: Iterable[ScratchSprite]=[]):
        condition = TimerCondition(reset_period,repeats)
        self.all_conditions.append(condition)
        self.all_triggers.append(condition.trigger)

        self.sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )                
        return condition
    
    
    def when_condition_met(self, checker=lambda: False, repeats=np.inf, associated_sprites: Iterable[ScratchSprite]=[]):
        condition = Condition(checker, repeats)
        self.all_conditions.append(condition)
        self.all_triggers.append(condition.trigger)

        self.sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )        
        return condition
    

    def create_trigger(self, associated_sprites: Iterable[ScratchSprite]=[]):

        trigger = Trigger()
        self.all_triggers.append(trigger)

        self.sprite_event_dependency_manager.add_event(
            trigger, associated_sprites
        )
        return trigger
    


    # change of behaviour

    def suppress_type_collision(self, collision_type, collision_suppressed=True):
        collision_allowed = not collision_suppressed

        if not collision_type in self.collision_type_to_trigger: 
            self.collision_type_to_trigger[collision_type] = collision_allowed, []    
        else:
            t_list = self.collision_type_to_trigger[collision_type][1]
            self.collision_type_to_trigger[collision_type] = collision_allowed, t_list

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

        self.current_time = 0


        for t in self.game_start_triggers:
            t.trigger()

        draw = True
        while True:
            dt = clock.tick(framerate*2)
            self.current_time += dt
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
                    t.handle_all(self.current_time)
                    # TODO: is it possible to remove t in the self.all_triggers here?
                    t.generators_proceed(self.current_time)

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

    def cleanup_old_shape(self, old_shape):
        remove_list = []
        for pair in self.contact_pairs_set:
            if old_shape in pair:
                remove_list.append(pair)
        self.contact_pairs_set.remove(*remove_list)
        
    def remove_sprite(self, sprite: ScratchSprite):

        self.all_sprites.remove(sprite)
        self.all_sprites_to_show.remove(sprite) 

        self.trigger_to_collision_pairs = {k: v for k, v in self.trigger_to_collision_pairs.items() if not sprite in v}

        
        self.cleanup_old_shape(sprite.shape)

        try: 
            self.space.remove(sprite.body, sprite.shape)
        except:
            print('removing non-existing shape or body')

        self.sprite_event_dependency_manager.sprite_removal(sprite)


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
            for t in self.backdrop_change_triggers:
                t.trigger(index)

    def next_backdrop(self):
        if not self.__backdrop_index is None: 
            self.switch_backdrop((self.__backdrop_index+1) % len(self.backdrops))
        


    
        
        
game = Game()

        