from __future__ import annotations
from os import PathLike

import numpy as np
import pygame
import pymunk
from .event import ConditionInterface, Trigger, Condition, TimerCondition, declare_callback_type
from pymunk.pygame_util import DrawOptions
from typing import Any, Callable, Generic, Iterable, Optional, List, Dict, ParamSpec, Set, Tuple, TypeVar, Union, cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sprite import Sprite



def _collision_begin(arbiter, space, data):
    game = cast(Game, data['game'])
    game._contact_pairs_set.add(arbiter.shapes) 

    for e, (a,b) in game._trigger_to_collision_pairs.items():
        if (a.shape in arbiter.shapes) and (b.shape in arbiter.shapes):
            e.trigger(arbiter)


    colliding_types = arbiter.shapes[0].collision_type, arbiter.shapes[1].collision_type
    collision_allowed = True
    for collision_type, (allowed, triggers) in game._collision_type_to_trigger.items():
        if collision_type in colliding_types: 
            [t.trigger(arbiter) for t in triggers]
            collision_allowed = collision_allowed and allowed
        

    if (arbiter.shapes[0].collision_type == 0) or (arbiter.shapes[1].collision_type == 0):
        collision_allowed = False


    return collision_allowed

def _collision_separate(arbiter, space, data):
    game = cast(Game, data['game'])

    if arbiter.shapes in game._contact_pairs_set:
        game._contact_pairs_set.remove(arbiter.shapes)


    reverse_order = arbiter.shapes[1], arbiter.shapes[0]
    if reverse_order in game._contact_pairs_set:
        game._contact_pairs_set.remove(reverse_order)


class CloneEventManager:
    """@private"""

    def __init__(self):
        # TODO: removed sprites stay here forever
        self.identical_sprites_and_triggers: List[Tuple[Set[Sprite], List[Trigger]]] = []

    def new_trigger(self, sprite:Sprite, trigger:Trigger):
        new_lineage = True
        for identical_sprites, triggers in self.identical_sprites_and_triggers:
            if sprite in identical_sprites: 
                new_lineage = False
                triggers.append(trigger)

        if new_lineage: 
            self.identical_sprites_and_triggers.append((set([sprite]), [trigger]))
                

    def on_clone(self, old_sprite:Sprite, new_sprite:Sprite):
        # so that the cloning of the cloned sprite will trigger the same event
        for identical_sprites, triggers in self.identical_sprites_and_triggers:
            if not old_sprite in identical_sprites:
                continue
            identical_sprites.add(new_sprite)

            for t in triggers:
                t.trigger(new_sprite)

        

class SpriteEventDependencyManager:
    """@private"""

    def __init__(self):

        self.sprites: Dict[Sprite, List[Union[Trigger, ConditionInterface]]] = {}

    def add_event(self, event: Union[ConditionInterface, Trigger], sprites: Iterable[Sprite]):
        """
        TODO: if the event is dependent to multiple sprites, the event will not be
        completely dereferenced until all the sprites on which it depends are removed

        """
        for s in sprites:
            if not s in self.sprites:
                self.sprites[s] = []
            self.sprites[s].append(event)


    def sprite_removal(self, sprite: Sprite):
        
        to_remove = self.sprites.get(sprite)
        if not to_remove:
            return 
    
        for e in to_remove:
            e.remove()

T = TypeVar('T')
"""@private"""
P = ParamSpec('P')
"""@private"""
class SpecificEventEmitter(Generic[P]):
    """@private"""

    def __init__(self):
        self.key2triggers: Dict[Any, List[Trigger[P]]] = {}

    def add_event(self, key, trigger:Trigger[P]):
        if not key in self.key2triggers: 
            self.key2triggers[key] = []
        self.key2triggers[key].append(trigger)
        

    def on_event(self, key, *args: P.args, **kwargs: P.kwargs):
        if not key in self.key2triggers: 
            return
        for t in self.key2triggers[key]:
            t.trigger(*args, **kwargs)



class Game:
    """
    This is the class that the `game` object belongs to. You cannot create another Game object. 
    """
    
    _singleton_lock = False
    def __init__(self, screen_size=(1280, 720)):
        """@private"""
        pygame.init()

        assert not Game._singleton_lock, "Already instantiated."
        Game._singleton_lock = True

        self._screen: pygame.Surface  = pygame.display.set_mode(screen_size, vsync=1)

        self._space: pymunk.Space = pymunk.Space()

        self._draw_options = DrawOptions(self._screen)

        # sounds
        self._mixer = pygame.mixer.init()

        self._sounds = {}

        # shared variables 
        self.shared_data: Dict[Any, Any] = {}
        """A dictionary of variables shared across the entire game. You can put anything in it."""
        
        # sprite event dependency manager
        self._sprite_event_dependency_manager = SpriteEventDependencyManager()

        # 
        self._clone_event_manager = CloneEventManager()
        """@private"""

        # collision detection
        self._trigger_to_collision_pairs = {}

        self._collision_type_pair_to_trigger: Dict[Tuple[int, int], List[Trigger]] = {}

        self._collision_type_to_trigger: Dict[int, Tuple[bool, List[Trigger]]] = {}

        self._contact_pairs_set: Set[Tuple[pymunk.Shape, pymunk.Shape]] = set() 


        self._collision_handler = self._space.add_default_collision_handler()

        self._collision_handler.data['game'] = self
        self._collision_handler.begin = _collision_begin
        self._collision_handler.separate = _collision_separate
        
        # sprites updating and drawing
        self._all_sprites = pygame.sprite.Group()

        self._all_sprites_to_show = pygame.sprite.LayeredUpdates()


        # # scheduled jobs
        # self.pre_scheduled_jobs = []
        # self.scheduled_jobs = []


        self._all_pygame_events = []

        self._all_triggers: List[Trigger] = [] # these are to be executed every iteration

        self._all_conditions: List[ConditionInterface] = [] # these are to be checked every iteration

        #self.all_forever_jobs: List[Callable[[], None]] = []
        self._all_message_subscriptions: Dict[str, List[Trigger]] = {}

        # key events 
        key_event = self.create_pygame_event_trigger([pygame.KEYDOWN, pygame.KEYUP])
        key_event.add_handler(self.__key_event_handler)
        self._all_simple_key_triggers: List[Trigger] = [] # these are to be triggered by self.__key_event_handler only

        # mouse dragging event
        self._dragged_sprite = None
        self._drag_offset = 0, 0

        self._sprite_click_trigger:Dict[Sprite, List[Trigger]] = {}  #TODO: need to be able to destory the trigger here when the sprite is destoryed
        mouse_drag_trigger = self.create_pygame_event_trigger([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        mouse_drag_trigger.add_handler(self.__mouse_drag_handler)

        ## Backdrops
        self.backdrops: List[pygame.Surface] = []

        self.__backdrop_index = None
        self._backdrop_change_triggers: List[Trigger] = []



        ## start event
        self._game_start_triggers: List[Trigger] = []

        ## global timer event
        self._global_timer_triggers: List[Trigger] = []

    
        self._current_time_ms: float = 0

        self._specific_key_event_emitter: SpecificEventEmitter[str] = SpecificEventEmitter()

        self._specific_backdrop_event_emitter: SpecificEventEmitter[[]] = SpecificEventEmitter()



    def __key_event_handler(self, e):
        up_or_down = 'down' if e.type == pygame.KEYDOWN else 'up'
        keyname = pygame.key.name(e.key)

        self._specific_key_event_emitter.on_event(keyname, up_or_down)

        for t in self._all_simple_key_triggers:
            t.trigger(keyname, up_or_down)



    def __mouse_drag_handler(self, e):

        if e.type == pygame.MOUSEBUTTONDOWN: 
            
            for s in reversed(list(self._all_sprites_to_show)):
                if TYPE_CHECKING:
                    s = cast(Sprite, s)
                if s.shape.point_query(e.pos).distance <= 0:
                    for t in self._sprite_click_trigger[s]:
                        t.trigger()

                    if not s.draggable:
                        continue

                    s._set_is_dragging (True)
                    self._dragged_sprite = s
                    offset_x = s.body.position[0]  - e.pos[0]
                    offset_y = s.body.position[1]  - e.pos[1]
                    self._drag_offset = offset_x, offset_y
                    break 

        elif e.type == pygame.MOUSEBUTTONUP:
            if self._dragged_sprite: 
                self._dragged_sprite._set_is_dragging(False)
                self._dragged_sprite = None

        elif e.type == pygame.MOUSEMOTION and self._dragged_sprite:
            x = e.pos[0] + self._drag_offset[0]
            y = e.pos[1] + self._drag_offset[1]
            self._dragged_sprite.set_xy((x,y))



    def update_screen_mode(self, *arg, **kwargs):
        """
        Update the screen, taking the arguments for [`pygame.display.set_mode`](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)
        

        Use this method to change the screen size:

        `game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`
        """
        self._screen  = pygame.display.set_mode( *arg, **kwargs)



    def start(self, framerate, sim_step_min=300, debug_draw=False, event_count=False):
        """
        Start the game. 

        Parameters
        ---
        framerate : int
            The number of frames per second

        sim_step_min: int
            The number of physics steps per second. Increase this value if the physics is unstable and decrease it if the game runs slow.
        
        debug_draw: bool
            Whether or not to draw the collision shape for debugging purposes

        event_count: bool
            Whether or not to print out the number of active events for debugging purposes

        """


        clock = pygame.time.Clock()

        draw_every_n_step = sim_step_min//framerate+1

        self._current_time_ms = 0


        for t in self._game_start_triggers:
            t.trigger()

        while True:
            dt = clock.tick(framerate)
            self._current_time_ms += dt
            for i in range(draw_every_n_step): 
                self._space.step(dt/draw_every_n_step)



            self._all_pygame_events = pygame.event.get()
            for event in self._all_pygame_events:
                if event.type == pygame.QUIT:
                    return 


            # for j in self.all_forever_jobs:
            #     j()

            # check conditions
            for c in self._all_conditions:
                c.check()

            # execute 
            for t in self._all_triggers:
                t.handle_all(self._current_time_ms)
                # TODO: is it possible to remove t in the self.all_triggers here?
                t.generators_proceed(self._current_time_ms)

            # clean up
            self._all_conditions = list(filter(lambda t: t.stay_active, self._all_conditions))
            self._all_simple_key_triggers = list(filter(lambda t: t.stay_active, self._all_simple_key_triggers))
            self._all_triggers = list(filter(lambda t: t.stay_active, self._all_triggers))

            
            if event_count: 
                print("all_conditions", len(self._all_conditions))
                print("all_triggers", len(self._all_triggers))
                print("all sprite", len(self._all_sprites))
                # print("all_simple_key_triggers", len(self.all_simple_key_triggers))

            # Drawing

            self._screen.fill((30, 30, 30))
            if not (self.__backdrop_index is None): 
                self._screen.blit(self.backdrops[self.__backdrop_index], (0, 0))

            if debug_draw: 
                self._space.debug_draw(self._draw_options)
            
            self._all_sprites.update(self._space)
            self._all_sprites_to_show.draw(self._screen)
            pygame.display.flip()



    def load_sound(self, key: str, path: PathLike) :
        """
        Load the sound given a path, and index it with the key so it can be played later by `play_sound`
        e.g. 
        ```python
        game.load_sound('sound1', 'path/to/sound.wav')
        game.play_sound('sound1', volume=0.5)
        ```
        """
        if key in self._sounds: 
            raise KeyError(f'{key} already loaded. Choose a different key name.')
        
        self._sounds[key] = pygame.mixer.Sound(path)

    def play_sound(self, key:str, volume=1.0):
        """
        Play the sound given a key. 
        This method does not wait for the sound to finish playing. 
        """        
        s = self._sounds[key]
        s.set_volume(volume)
        s.play()
    
    
    def read_timer(self) -> float:
        """get the time since the game started"""
        return self._current_time_ms/1000
    

    def set_gravity(self, xy: Tuple[float, float]):
        """
        Change the gravity of the space. Works for sprites with dynamic body type only.
        """
        self._space.gravity = xy

    def add_sprite(self, sprite, to_show=True):

        self._all_sprites.add(sprite)
        #self._space.add(sprite.body, sprite.shape)
        self._sprite_click_trigger[sprite] = []
        if to_show:
            self._all_sprites_to_show.add(sprite)

    def cleanup_old_shape(self, old_shape):

        remove_list = []
        for pair in self._contact_pairs_set:
            if old_shape in pair:
                remove_list.append(pair)

        for r in remove_list:
            self._contact_pairs_set.remove(r)
        
    def remove_sprite(self, sprite: Sprite):

        self._all_sprites.remove(sprite)
        self._all_sprites_to_show.remove(sprite) 

        self._trigger_to_collision_pairs = {k: v for k, v in self._trigger_to_collision_pairs.items() if not sprite in v}

        
        self.cleanup_old_shape(sprite.shape)

        try: 
            self._space.remove(sprite.body, sprite.shape)
        except:
            print('removing non-existing shape or body')

        self._sprite_event_dependency_manager.sprite_removal(sprite)


    def show_sprite(self, sprite):

        self._all_sprites_to_show.add(sprite)

    def hide_sprite(self, sprite):

        self._all_sprites_to_show.remove(sprite)

    def bring_to_front(self, sprite):
        self._all_sprites_to_show.move_to_front(sprite)

    def move_to_back(self, sprite):
        self._all_sprites_to_show.move_to_back(sprite)

    def change_layer(self, sprite, layer):
        self._all_sprites_to_show.change_layer(sprite, layer)


    def change_layer_by(self, sprite, by):
        layer = self._all_sprites_to_show.get_layer_of_sprite(sprite)
        self._all_sprites_to_show.change_layer(sprite, layer + by)

    def get_layer_of_sprite(self, sprite):
        self._all_sprites_to_show.get_layer_of_sprite(sprite)

    def set_backdrops(self, images: List[pygame.Surface]):
        self.backdrops = images
    
    @property
    def backdrop_index(self):
        return self.__backdrop_index

    def switch_backdrop(self, index:Optional[int]=None):

        if index != self.__backdrop_index:
            self.__backdrop_index = index
            for t in self._backdrop_change_triggers:
                t.trigger(index)
            self._specific_backdrop_event_emitter.on_event(self.__backdrop_index)

    def next_backdrop(self):
        if not self.__backdrop_index is None: 
            self.switch_backdrop((self.__backdrop_index+1) % len(self.backdrops))
        



    # all events 

    ## scratch events

    def when_game_start(self, associated_sprites : Iterable[Sprite]=[]):

        t = self.create_trigger(associated_sprites)
        self._game_start_triggers.append(t)

        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = declare_callback_type(t, sample_callback)
        return t
            
    
    def when_any_key_pressed(self, associated_sprites : Iterable[Sprite]=[]) -> Trigger[[str, str]]:
        """
        Catch all keys and catch both press and release. 
        Returns an event (a `Trigger` object) that takes in two str argments
        """
        t = self.create_trigger(associated_sprites)
        self._all_simple_key_triggers.append(t)

        if TYPE_CHECKING:
            def sample_callback(key:str, updown:str)-> Any:
                return
            # this way the naming of the parameters is constrained too
            t = declare_callback_type(t, sample_callback)
            #t = cast(Trigger[[str, str]], t)

        return t
    
    def when_key_pressed(self, key, associated_sprites : Iterable[Sprite]=[])-> Trigger[[str]]:
        t = self.create_trigger(associated_sprites)

        if TYPE_CHECKING:
            def sample_callback(updown:str)-> Any:
                return
            # this way the naming of the parameters is constrained too
            t = declare_callback_type(t, sample_callback)

        self._specific_key_event_emitter.add_event(key, t)
        return t    
    
    def when_this_sprite_clicked(self, sprite, other_associated_sprites: Iterable[Sprite]=[]):
        t = self.create_trigger(set(list(other_associated_sprites)+[sprite]))

        if not sprite in self._sprite_click_trigger:
            self._sprite_click_trigger[sprite] = []
            
        self._sprite_click_trigger[sprite].append(t)
        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = declare_callback_type(t, sample_callback)
        return t
    
    def when_backdrop_switched(self, backdrop_index, associated_sprites : Iterable[Sprite]=[]):
        t = self.create_trigger(associated_sprites)

        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = declare_callback_type(t, sample_callback)

        self._specific_backdrop_event_emitter.add_event(backdrop_index, t)
        return t
 
    def when_any_backdrop_switched(self, associated_sprites : Iterable[Sprite]=[]):
        """different to scratch: catch all switches"""
        t = self.create_trigger(associated_sprites)
        self._backdrop_change_triggers.append(t)
        if TYPE_CHECKING:
            def sample_callback(idx: int)-> Any:
                return
            t = declare_callback_type(t, sample_callback)

        return t

    def when_timer_above(self, t, associated_sprites : Iterable[Sprite]=[]):
        return self.when_condition_met(lambda:(self._current_time_ms>t), 1, associated_sprites)
    
    def when_receive_message(self, topic: str, associated_sprites : Iterable[Sprite]=[]):
        trigger = self.create_trigger(associated_sprites)
        self.__new_subscription(topic, trigger)
        if TYPE_CHECKING:
            def sample_callback(data: Any)-> Any:
                return
            trigger = declare_callback_type(trigger, sample_callback)
        return trigger
    
    def when_started_as_clone(self, sprite, associated_sprites : Iterable[Sprite]=[]):
        trigger = self.create_trigger(associated_sprites)
        self._clone_event_manager.new_trigger(sprite, trigger)
        if TYPE_CHECKING:
            def sample_callback(clone_sprite: Sprite)-> Any:
                return
            trigger = declare_callback_type(trigger, sample_callback)
        return trigger

    
    def broadcast_message(self, topic: str, data: Any):
        if not topic in self._all_message_subscriptions:
            return 
        
        self._all_message_subscriptions[topic] = list(filter(lambda t: t.stay_active, self._all_message_subscriptions[topic]))
        for e in self._all_message_subscriptions[topic]:
            e.trigger(data)

    def __new_subscription(self, topic: str, trigger: Trigger):
        if not (topic in self._all_message_subscriptions):
            self._all_message_subscriptions[topic] = []

        self._all_message_subscriptions[topic].append(trigger)



    ## advance events
    def create_pygame_event_trigger(self, flags: List[int], associated_sprites : Iterable[Sprite]=[]):

        condition = self.when_condition_met(associated_sprites)
        
        def checker_hijack():
            for e in self._all_pygame_events:
                if e.type in flags:
                    condition.trigger.trigger(e)

            if not condition.trigger.stay_active:
                condition.remove()

        condition.change_checker(checker_hijack)
        return condition.trigger


    def create_specific_collision_trigger(self, sprite1: Sprite, sprite2: Sprite, other_associated_sprites: Iterable[Sprite]=[]):

        #"""Cannot change the collision type of the object after calling this function"""
        trigger = self.create_trigger(set(list(other_associated_sprites)+[sprite1, sprite2]))

        self._trigger_to_collision_pairs[trigger] = sprite1, sprite2

     
        return trigger

    def create_type2type_collision_trigger(self, type_a:int, type_b:int, collision_suppressed=False, associated_sprites: Iterable[Sprite]=[]):
        pair = (type_a, type_b) if type_a>type_b else (type_b, type_a)

        h = self._space.add_collision_handler(*pair)
        trigger = self.create_trigger(associated_sprites)



        if not pair in self._collision_type_pair_to_trigger: 
            self._collision_type_pair_to_trigger[pair] = []
        self._collision_type_pair_to_trigger[pair].append(trigger)

        collision_allowed = not collision_suppressed
        def begin(arbiter, space, data):
            game = cast(Game, data['game'])
            game._contact_pairs_set.add(arbiter.shapes) 

            for t in game._collision_type_pair_to_trigger[pair]:
                t.trigger(arbiter)
            return collision_allowed
        
        h.data['game'] = self
        h.begin = begin
        h.separate = _collision_separate

        
        return trigger


    def create_type_collision_trigger(self, collision_type:int , collision_suppressed=False, associated_sprites: Iterable[Sprite]=[]):
        trigger = self.create_trigger(associated_sprites)

        collision_allowed = not collision_suppressed
        

        if not collision_type in self._collision_type_to_trigger: 
            self._collision_type_to_trigger[collision_type] = collision_allowed, []


        self._collision_type_to_trigger[collision_type][1].append(trigger)

        return trigger
    

    def when_timer_reset(self, reset_period=np.inf, repeats=np.inf, associated_sprites: Iterable[Sprite]=[]):
        condition = TimerCondition(reset_period,repeats)
        self._all_conditions.append(condition)
        self._all_triggers.append(condition.trigger)

        self._sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )                
        return condition
    
    
    def when_condition_met(self, checker=lambda: False, repeats=np.inf, associated_sprites: Iterable[Sprite]=[]):
        condition = Condition(checker, repeats)
        self._all_conditions.append(condition)
        self._all_triggers.append(condition.trigger)

        self._sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )        
        return condition
    

    def create_trigger(self, associated_sprites: Iterable[Sprite]=[]) -> Trigger:

        trigger = Trigger()
        self._all_triggers.append(trigger)

        self._sprite_event_dependency_manager.add_event(
            trigger, associated_sprites
        )
        return trigger
    


    # change of behaviour

    def suppress_type_collision(self, collision_type, collision_suppressed=True):
        collision_allowed = not collision_suppressed

        if not collision_type in self._collision_type_to_trigger: 
            self._collision_type_to_trigger[collision_type] = collision_allowed, []    
        else:
            t_list = self._collision_type_to_trigger[collision_type][1]
            self._collision_type_to_trigger[collision_type] = collision_allowed, t_list

game = Game()
"""
The singleton Game object. This is the object that represent the game.   
"""
        