"""
Everything in this module is directly under the pyscratch namespace. 
For example, instead of doing `pysc.game_module.is_key_pressed`,
you can also directly do `pysc.is_key_pressed`.
"""

from __future__ import annotations
from functools import cache
from os import PathLike
import os
from pathlib import Path
import threading
import time
import json, inspect
from typing_extensions import deprecated

import numpy as np
import pygame
import pymunk
from .event import _ConditionInterface, Event, Condition, TimerCondition, _declare_callback_type
from pymunk.pygame_util import DrawOptions
from typing import Any, Callable, Generic, Iterable, Literal, Optional, List, Dict, ParamSpec, Set, Tuple, TypeVar, Union, cast
from typing import TYPE_CHECKING
from . import helper

if TYPE_CHECKING:
    from .sprite import Sprite

def _collision_begin(arbiter, space, data):
    game = cast(Game, data['game'])
    game._contact_pairs_set.add(arbiter.shapes) 

    for e, (a,b) in game._trigger_to_collision_pairs.items():
        if (a._shape in arbiter.shapes) and (b._shape in arbiter.shapes):
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


class _CloneEventManager:

    def __init__(self):
        # TODO: removed sprites stay here forever
        self.identical_sprites_and_triggers: List[Tuple[Set[Sprite], List[Event]]] = []

    def new_trigger(self, sprite:Sprite, trigger:Event):
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

        

class _SpriteEventDependencyManager:

    def __init__(self):

        self.sprites: Dict[Sprite, List[Union[Event, _ConditionInterface]]] = {}

    def add_event(self, event: Union[_ConditionInterface, Event], sprites: Iterable[Sprite]):
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

class _SpecificEventEmitter(Generic[P]):

    def __init__(self):
        self.key2triggers: Dict[Any, List[Event[P]]] = {}

    def add_event(self, key, trigger:Event[P]):
        if not key in self.key2triggers: 
            self.key2triggers[key] = []
        self.key2triggers[key].append(trigger)
        

    def on_event(self, key, *args: P.args, **kwargs: P.kwargs):
        if not key in self.key2triggers: 
            return
        for t in self.key2triggers[key]:
            t.trigger(*args, **kwargs)



class _SavedSpriteStateManager:
    default_filename = "saved_sprite_states.json"
    def __init__(self):
        self.states: Dict[str, Dict[str, Any]]  = {}


    def save_sprite_states(self, all_sprite: Iterable[Sprite], filename=None):
        """
        Save the x, y & direction of the sprites. 

        Usage: 
        ```python
        # main.py
        from pyscratch import game

        game.start() # when you close the game window, the game.start() function finishes.
        game.save_sprite_states() # then this function will be run.   
        
        ```
        """
        loc = {}
        for s in all_sprite:
            loc[s.identifier] = dict(x=s.x, y=s.y, direction=s.direction)

        if not filename:
            filename = self.default_filename
        #caller_file = Path(inspect.stack()[-1].filename)

        json.dump(loc, open(filename, "w"))
        print("Sprite states saved.")
    
    def load_saved_state(self, filename=None):

        if not filename:
            filename = self.default_filename
            
        filename = Path(filename)
        if filename.exists():
            self.states= json.load(open(filename, "r"))


    def get_state_of(self, sprite_id):

        return self.states.get(sprite_id)
    

class Game:
    """
    This is the class that the `game` object belongs to. You cannot create another Game object. 
    To exit the game, either close the window, or to press the escape key (esc) by default
    """
    
    _singleton_lock = False
    def __init__(self):
        """@private"""
        pygame.init()

        assert not Game._singleton_lock, "Already instantiated."
        Game._singleton_lock = True

        # the screen is needed to load the images. 
        self._screen: pygame.Surface  = pygame.display.set_mode((1280, 720), vsync=1)

        self._space: pymunk.Space = pymunk.Space()


        self._draw_options = DrawOptions(self._screen)

        # sounds
        self._mixer = pygame.mixer.init()

        self._sounds = {}

        # shared variables 
        self.shared_data: Dict[Any, Any] = {}
        """
        A dictionary of variables shared across the entire game. You can put anything in it.
        
        The access of the items can be done directly through the game object. 
        For example, `game['my_data'] = "hello"` is just an alias of `game.shared_data['my_data'] = "hello"` 
        
        Bare in mind that the order of executions of different events and different files is arbitrary. 
        Therefore if variable is defined in one event and accessed in another, 
        a KeyError may be raised because variables are only accessible after the definition. 

        Instead, the all the variable should be defined outside the event (before the game start),
        and variables should be accessed only within events to guarantee its definition. 


        Example:
        ```python
        from pyscratch import game 

        # same as `game.shared_data['score_left'] = 0`
        game['score_left'] = 0
        game['score_right'] = 0

        def on_score(side):
            if side == "left":
                game['score_left'] += 1
            else:
                game['score_right'] += 1

            print(f"Left score: {game['score_left']}") 
            print(f"Right score: {game['score_right']}") 

        game.when_received_message('score').add_handler(on_score)
        game.broadcast_message('on_score', 'left')
        ```
        """
        
        # sprite event dependency manager
        self._sprite_event_dependency_manager = _SpriteEventDependencyManager()

        # 
        self._clone_event_manager = _CloneEventManager()
        """@private"""

        # collision detection
        self._trigger_to_collision_pairs: Dict[Event, Tuple[Sprite, Sprite]] = {}

        self._collision_type_pair_to_trigger: Dict[Tuple[int, int], List[Event]] = {}

        self._collision_type_to_trigger: Dict[int, Tuple[bool, List[Event]]] = {}

        self._contact_pairs_set: Set[Tuple[pymunk.Shape, pymunk.Shape]] = set() 


        self._collision_handler = self._space.add_default_collision_handler()

        self._collision_handler.data['game'] = self
        self._collision_handler.begin = _collision_begin
        self._collision_handler.separate = _collision_separate
        
        # sprites updating and drawing
        self._all_sprites = pygame.sprite.Group()

        self._all_sprites_to_show = pygame.sprite.LayeredUpdates(default_layer=1)


        # # scheduled jobs
        # self.pre_scheduled_jobs = []
        # self.scheduled_jobs = []


        self._all_pygame_events = []

        self._all_triggers: List[Event] = [] # these are to be executed every iteration

        self._all_conditions: List[_ConditionInterface] = [] # these are to be checked every iteration

        #self.all_forever_jobs: List[Callable[[], None]] = []
        self._all_message_subscriptions: Dict[str, List[Event]] = {}

        # key events 
        key_event = self.create_pygame_event([pygame.KEYDOWN, pygame.KEYUP])
        key_event.add_handler(self.__key_event_handler)
        self._all_simple_key_triggers: List[Event] = [] # these are to be triggered by self.__key_event_handler only

        # mouse dragging event
        self._dragged_sprite = None
        self._drag_offset = 0, 0
        self.__clicked_sprite =  None
        self._sprite_click_release_trigger:Dict[Sprite, List[Event]] = {}  #TODO: need to be able to destory the trigger here when the sprite is destoryed

        self._sprite_click_trigger:Dict[Sprite, List[Event]] = {}  #TODO: need to be able to destory the trigger here when the sprite is destoryed
        self._mouse_drag_trigger = self.create_pygame_event([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        self._mouse_drag_trigger.add_handler(self.__mouse_drag_handler)

        # Backdrops
        self.backdrops_by_key: Dict[str, pygame.Surface] = {}
        self.backdrop_indices_by_key: Dict[str, int] = {}
        self.backdrop_keys: List[str] = []

# TODO: testing needed

        self.__screen_width: int = 0
        self.__screen_height: int = 0
        self.__framerate: float = 0

        # TODO index and key need to be changed together 
        # the index is remained for the next_backdrop function
        self.__backdrop_index = None
        self.__backdrop_key = None

        # TODO: the event is now triggered by the name not the index
        self._backdrop_change_triggers: List[Event] = []

        self._top_edge: Sprite
        self._left_edge: Sprite
        self._bottom_edge: Sprite
        self._right_edge: Sprite


        ## start event
        self._game_start_triggers: List[Event] = []

        ## global timer event
        self._global_timer_triggers: List[Event] = []

    
        self._current_time_ms: float = 0

        self._specific_key_event_emitter: _SpecificEventEmitter[str] = _SpecificEventEmitter()

        self._specific_backdrop_event_emitter: _SpecificEventEmitter[[]] = _SpecificEventEmitter()

        self.max_number_sprite = 1000
        """The maximum number of sprites in the game. Adding more sprites will lead to an error to prevent freezing. Default to 1000."""
        
        self._sprite_count_per_file: Dict[str, int] = {}

        self.__start = False
        """set to false to end the loop"""


        self.update_screen_mode()

        self._saved_states_manager = _SavedSpriteStateManager()
        self.__sprite_last_clicked_for_removal: Optional[Sprite] = None
        self.__started_interactive = False


    def __key_event_handler(self, e):
        up_or_down = 'down' if e.type == pygame.KEYDOWN else 'up'
        keyname = pygame.key.name(e.key)

        self._specific_key_event_emitter.on_event(keyname, up_or_down)

        for t in self._all_simple_key_triggers:
            t.trigger(keyname, up_or_down)

    def __getitem__(self, key):
        return self.shared_data[key]
    
    def __setitem__(self, k, v):
        self.shared_data[k] = v


    def __mouse_drag_handler(self, e):

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 

            for s in reversed(list(self._all_sprites_to_show)):
                if TYPE_CHECKING:
                    s = cast(Sprite, s)
                    
                # click is on the top sprite only
                if s.is_touching_mouse():
                    self.__clicked_sprite = s
                    self.__sprite_last_clicked_for_removal = s

                    for t in self._sprite_click_trigger[s]:
                        t.trigger()

                    if not s.draggable:
                        break
                    
                    s._set_is_dragging (True)
                    self._dragged_sprite = s
                    offset_x = s._body.position[0]  - e.pos[0]
                    offset_y = s._body.position[1]  - e.pos[1]
                    self._drag_offset = offset_x, offset_y
                    break 



        elif e.type == pygame.MOUSEBUTTONUP  and e.button == 1:
            if self._dragged_sprite: 
                self._dragged_sprite._set_is_dragging(False)
                self._dragged_sprite = None

            # TODO: what happens here?? why AND?
            if self.__clicked_sprite and (temp:= self._sprite_click_release_trigger.get(self.__clicked_sprite)):
                #temp  =  self._sprite_click_release_trigger.get(self.__clicked_sprite)
                #if temp: 
                for t in temp:
                    t.trigger()
                self.__clicked_sprite = None

        elif e.type == pygame.MOUSEMOTION and self._dragged_sprite:
            x = e.pos[0] + self._drag_offset[0]
            y = e.pos[1] + self._drag_offset[1]
            self._dragged_sprite.set_xy((x,y))



    def update_screen_mode(self, *arg, **kwargs):
        """
        Update the screen, taking the arguments for 
        [`pygame.display.set_mode`](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode).
        

        Use this method to change the screen size:

        `game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`
        """
        self.__screen_args = arg
        self.__screen_kwargs = kwargs
        
    @property
    def screen_width(self):
        """The width of the screen. Not available until the game is started (should not be referenced outside events)."""
        return self.__screen_width
    
    @property
    def screen_height(self):
        """The height of the screen. Not available until the game is started (should not referenced outside events)."""
        return self.__screen_height
    
    @property
    def framerate(self):
        """The frame rate of the game. Not available until the game is started"""
        return self.__framerate
    
    def _do_autoremove(self):
        for s in self._all_sprites:
            if ((s.x < -s.oob_limit) or 
             (s.x > (s.oob_limit + self.__screen_width)) or 
             (s.y < -s.oob_limit) or 
             (s.y > (s.oob_limit + self.__screen_height)) 
            ):     
                #print(s.x, s.y)
                #print(s.oob_limit + self.__screen_width, s.oob_limit + self.__screen_height)
                s.remove()
                print(f"{s} is removed for going out of boundary above the specified limit.")

    def _check_alive(self):

        last_frame_time = 0
        while True:

            for i in range(10):
                time.sleep(.2)
                if not self.__start:
                    return 
            if not self._current_time_ms > last_frame_time:
                print('Stucked in the same frame for more than 1 second. This can happen when an error occur or you are in a infinite loop without yielding. ')
                os._exit(1)

            last_frame_time = self._current_time_ms

    def start_interactive(self, *args, sprite_removal_key='backspace', **kwargs):
        """
        @private
        Start the game on another thread for jupyter notebook (experimental)
        """ 
        if self.__started_interactive: 
            raise RuntimeError("The game must not be restarted. Please restart the kernal. ")
        self.__started_interactive = True    
        
        def remove_sprite(_):
            if s:=self.__clicked_sprite: 
                s.remove()

        self.when_key_pressed(sprite_removal_key).add_handler(remove_sprite)

        t = threading.Thread(target=self.start, args=args, kwargs=kwargs)
        t.start()
        self.__screen_thread = t
        
        
        return t
    
    def stop(self):
        """
        @private
        """
        self.__start = False
        if self.__started_interactive:
            #self.__started_interactive = False
            pygame.display.quit()
        

    def start(
            self, 
            framerate=30, 
            sim_step_min=300, 
            debug_draw=False, 
            event_count=False, 
            show_mouse_position: Optional[bool]=None, 
            exit_key: Optional[str]="escape",
            saved_state_file=None, 
            print_fps = False,
            use_frame_time = False
        ):
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

        show_mouse_position: bool
            Whether or not to show the mouse position in the buttom-right corner

        exit_key: Optional[str]
            Very useful if you are working on a fullscreen game
            Set to None to disable it.

        saved_state_file: Optional[str]
            The path of the saved state. Default location will be used if set to None. 

        print_fps: bool
            Whether or not to print the fps

        use_frame_time: bool
            Use the number of frames to define game time. Note: highly experimental. 

        """

        if not (len(self.__screen_args) or len(self.__screen_kwargs)):
            self.__screen_kwargs = dict(size=(1280, 720))

        self._screen  = pygame.display.set_mode(*self.__screen_args, **self.__screen_kwargs)

        self._saved_states_manager.load_saved_state(saved_state_file)
        self.__framerate = framerate
        self.__screen_width = self._screen.get_width()
        self.__screen_height = self._screen.get_height()

        guide_lines_font = pygame.font.Font(None, 30)

        clock = pygame.time.Clock()

        

        draw_every_n_step = sim_step_min//framerate+1

        self._current_time_ms = 0

        if exit_key:
            self.when_key_pressed(exit_key).add_handler(lambda _: self.stop())
            
        self.create_pygame_event([pygame.QUIT]).add_handler(lambda _: self.stop())
        
        for t in self._game_start_triggers:
            t.trigger()

        cleanup_period = 2*framerate
        loop_count = 0

        threading.Thread(target=self._check_alive).start()
        frame_interval = 1000/framerate

        self.__start = True
        while self.__start:
            if print_fps:
                print(f"FPS: {clock.get_fps()}")            
            loop_count += 1
            
            dt = clock.tick(framerate)
            self._current_time_ms += frame_interval if use_frame_time else dt 
            for i in range(draw_every_n_step): 
                self._space.step(dt/draw_every_n_step)

            self._all_pygame_events = pygame.event.get()


            # check conditions
            for c in self._all_conditions:
                c._check()

            # execute 
            for t in self._all_triggers:
                t._handle_all(self._current_time_ms)
                # TODO: is it possible to remove t in the self.all_triggers here?
                t._generators_proceed(self._current_time_ms)

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

            #self._screen.fill((30, 30, 30))
            if not (self.__backdrop_key is None): 
                self._screen.blit(self.backdrops_by_key[self.__backdrop_key], (0, 0))
            else:
                self._screen.fill((255,255,255))
                helper._draw_guide_lines(self._screen, guide_lines_font, 100, 500)

                if show_mouse_position is None: 
                    helper._show_mouse_position(self._screen, guide_lines_font)

            if debug_draw: 
                self._space.debug_draw(self._draw_options)

            self._all_sprites.update()
            #self._all_sprites_to_show.update()
            self._all_sprites_to_show.draw(self._screen)

            if show_mouse_position:
                helper._show_mouse_position(self._screen, guide_lines_font)


            pygame.display.flip()
            if not loop_count % cleanup_period:
                self._do_autoremove()

    def _get_saved_state(self, sprite_id):
        return self._saved_states_manager.get_state_of(sprite_id)

    def save_sprite_states(self):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Save the x, y & direction of the sprites.

        To retrieve the states of the sprites, refer to [`retrieve_saved_state`](./sprite#Sprite.retrieve_saved_state)


        Usage:
        ```python
        from pyscratch import game

        # Start the game. The program stays in this line until the game window is closed. 
        game.start(60)

        # The program will get to this line when the game window is closed normally (not due to an error). 
        game.save_sprite_states()
        ```

        """
        self._saved_states_manager.save_sprite_states(self._all_sprites)

    def load_sound(self, key: str, path: str) :
        """
        Load the sound given a path, and index it with the key so it can be played later by `play_sound`

        Example:
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

        Example:
        ```python
        game.load_sound('sound1', 'path/to/sound.wav')
        game.play_sound('sound1', volume=0.5)
        ```        
        """        
        s = self._sounds[key]
        s.set_volume(volume)
        s.play()
    
    
    def read_timer(self) -> float:
        """get the time (in seconds) since the game started."""
        return self._current_time_ms/1000
    

    def set_gravity(self, xy: Tuple[float, float]):
        """
        @private
        *EXTENDED FEATURE*
        
        Change the gravity of the space. Works for sprites with dynamic body type only, which is not the default.
        It will NOT work unless you explicitly make the sprite to have a dynamic body. 
        """
        self._space.gravity = xy

    def _new_sprite_of_file(self, caller_file):
        """
        return a index of the sprite created in the file
        """
        if not caller_file in self._sprite_count_per_file:
            self._sprite_count_per_file[caller_file] = 0
        else: 
            self._sprite_count_per_file[caller_file] += 1

        return self._sprite_count_per_file[caller_file]


    def _add_sprite(self, sprite: Sprite, caller_file=None):

        self._all_sprites.add(sprite)
        if len(self._all_sprites) > self.max_number_sprite:
            raise RuntimeError('Reached the maximum number sprite. ')
        #self._space.add(sprite.body, sprite.shape)
        self._sprite_click_trigger[sprite] = []
        # if to_show:
        #     sprite.show()
            #self._all_sprites_to_show.add(sprite)
        #sprite.update()

        if self.__started_interactive:
            sprite.set_draggable(True)

        return self._new_sprite_of_file(caller_file)

    def _cleanup_old_shape(self, old_shape):

        remove_list = []
        for pair in self._contact_pairs_set:
            if old_shape in pair:
                remove_list.append(pair)

        for r in remove_list:
            self._contact_pairs_set.remove(r)
        
    def _remove_sprite(self, sprite: Sprite):
        """
        Remove the sprite from the game.

        You can use the alias `Sprite.remove()` to do the same. 
        """

        self._all_sprites.remove(sprite)
        self._all_sprites_to_show.remove(sprite) 

        self._trigger_to_collision_pairs = {k: v for k, v in self._trigger_to_collision_pairs.items() if not sprite in v}

        
        self._cleanup_old_shape(sprite._shape)

        try: 
            self._space.remove(sprite._body, sprite._shape)
        except:
            print('removing non-existing shape or body')

        self._sprite_event_dependency_manager.sprite_removal(sprite)


    def _show_sprite(self, sprite: Sprite):
        """
        Show the sprite. 
        """
        self._all_sprites_to_show.add(sprite)

    def _hide_sprite(self, sprite: Sprite):
        """
        Hide the sprite. 
        """
        self._all_sprites_to_show.remove(sprite)

    def bring_to_front(self, sprite: Sprite):
        """
        Bring the sprite to the front. 
        Analogous to the "go to [front] layer" block in Scratch
        """
        #self._all_sprites_to_show.move_to_front(sprite)
        new_top_layer = self._all_sprites_to_show.get_top_layer()+1
        self.change_layer(sprite, new_top_layer)


    def move_to_back(self, sprite: Sprite):
        """
        Move the sprite to the back. 
        Analogous to the "go to [back] layer" block in Scratch
        """        
        self._all_sprites_to_show.move_to_back(sprite)
        sprite._assign_layer(0)

    def change_layer(self, sprite: Sprite, layer: int):
        """
        Bring the sprite to a specific layer. 
        """              
        self._all_sprites_to_show.change_layer(sprite, layer)
        sprite._assign_layer(layer)


    def change_layer_by(self, sprite: Sprite, by: int):
        """
        Analogous to the "go to [forward/backward] [N] layer" block in Scratch
        """           
        layer = self._all_sprites_to_show.get_layer_of_sprite(sprite)
        self._all_sprites_to_show.change_layer(sprite, layer + by)
        sprite._assign_layer(layer + by)


    def get_layer_of_sprite(self, sprite: Sprite):
        """
        Returns the layer number of the given sprite
        """
        self._all_sprites_to_show.get_layer_of_sprite(sprite)

    @deprecated("use add_backdrop")
    def set_backdrops(self, images: List[pygame.Surface]):
        """
        Set the list of all available backdrops. This function is meant to be run before the game start. 
        
        Example: 
        ```python
        # load the image into python 
        background_image = pysc.load_image('assets/my_background.jpg')
        background_image2 = pysc.load_image('assets/my_background2.jpg')
        background_image3 = pysc.load_image('assets/my_background3.jpg')

        # pass in a list of all the available backdrops. 
        pysc.game.set_backdrops([background_image, background_image2, background_image3])

        # choose the backdrop at index 1 (background_image2)
        pysc.game.switch_backdrop(1) 
        ```
        """
        for idx, img in enumerate(images):
            self.add_backdrop(str(idx), img)

    def add_backdrop(self, key, image: pygame.Surface):
        """
        Add the image as a backdrop, and index it with the key so it can be switched to using switch_backdrop 

        Example:
        ```python
        bg0 = pysc.load_image("assets/undersea_bg.png")'

        game.add_backdrop('background0', bg0)
        game.switch_backdrop('background0')
        ```

        """
        assert not key in self.backdrops_by_key, f"the name '{key}' is already in used"
        self.backdrop_keys.append(key)
        self.backdrops_by_key[key] = image
        self.backdrop_indices_by_key[key] = len(self.backdrop_keys) - 1 # minus one since the new one is added in the previous line
        

    @property
    def backdrop_index(self):
        """
        The index of the current backdrops. 
        """
        return self.__backdrop_index
    

    @property
    def backdrop_key(self):
        """
        The key (i.e. name) of the current backdrops.
        """
        return self.__backdrop_key
    
    def switch_backdrop(self, key:Optional[str]=None):
        """
        Change the backdrop by specifying the key of the backdrop.  
        """
        # backward compatibilty for v1
        if isinstance(key, int):
            key = str(key)
        if key != self.__backdrop_key:
            self.__backdrop_key = key
            self.__backdrop_index = None if key is None else self.backdrop_indices_by_key[key] 
            for t in self._backdrop_change_triggers:
                t.trigger(key)
            self._specific_backdrop_event_emitter.on_event(key)

    # TODO: testing needed
    def next_backdrop(self):
        """
        Switch to the next backdrop. 
        """
        if not self.__backdrop_index is None: 
            idx = (self.__backdrop_index+1) % len(self.backdrops_by_key)
            self.switch_backdrop(self.backdrop_keys[idx])
        
    # all events 

    ## scratch events

    def when_game_start(self, associated_sprites : Iterable[Sprite]=[])->Event[[]]:
        """
        It is recommended to use the `Sprite.when_game_start` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.

        Returns an `Event` that is triggered when you call `game.start`. 
        The event handler does not take in any parameter.

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        

        t = self._create_event(associated_sprites)
        self._game_start_triggers.append(t)

        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = _declare_callback_type(t, sample_callback)
        return t
            
    
    def when_any_key_pressed(self, associated_sprites : Iterable[Sprite]=[]) -> Event[[str, str]]:
        """
        It is recommended to use the `Sprite.when_any_key_pressed` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  

        Returns an `Event` that is triggered when a key is pressed or released. 
        
        The event handler have to take two parameters:
        - **key** (str): The key that is pressed. For example, 'w', 'd', 'left', 'right', 'space'. 
            Uses [pygame.key.key_code](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) under the hood. 
        
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a press or a release

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
    
        """
        t = self._create_event(associated_sprites)
        self._all_simple_key_triggers.append(t)

        if TYPE_CHECKING:
            def sample_callback(key:str, updown:str)-> Any:
                return
            # this way the naming of the parameters is constrained too
            t = _declare_callback_type(t, sample_callback)
            #t = cast(Trigger[[str, str]], t)

        return t
    
    def when_key_pressed(self, key, associated_sprites : Iterable[Sprite]=[])-> Event[[str]]:
        """
        It is recommended to use the `Sprite.when_key_pressed` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  
        
        Returns an `Event` that is triggered when a specific key is pressed or released. 

        The event handler have to take one parameter:
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a press or a release
        
        Parameters
        ---
        key: str
            The key that triggers the event. For example, 'w', 'd', 'left', 'right', 'space'. 
            Uses [pygame.key.key_code](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) under the hood. 

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        t = self._create_event(associated_sprites)

        if TYPE_CHECKING:
            def sample_callback(updown:str)-> Any:
                return
            # this way the naming of the parameters is constrained too
            t = _declare_callback_type(t, sample_callback)

        self._specific_key_event_emitter.add_event(key, t)
        return t    
    
    def when_this_sprite_clicked(self, sprite, other_associated_sprites: Iterable[Sprite]=[]) -> Event[[]]:
        """
        It is recommended to use the `Sprite.when_this_sprite_clicked` alias instead of this method.
        
        Returns an `Event` that is triggered when the given sprite is clicked by mouse.  
        The event handler does not take in any parameter.

        Parameters
        ---
        sprite: Sprite
            The sprite on which you want the click to be detected. The removal of this sprite will lead to the removal of this event so
            it does not need to be included in `other_assoicated_sprite`
        
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        t = self._create_event(set(list(other_associated_sprites)+[sprite]))

        if not sprite in self._sprite_click_trigger:
            self._sprite_click_trigger[sprite] = []
            
        self._sprite_click_trigger[sprite].append(t)
        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = _declare_callback_type(t, sample_callback)
        return t
    

    def when_this_sprite_click_released(self, sprite, other_associated_sprites: Iterable[Sprite]=[]) -> Event[[]]:
        """
        The alias `Sprite.when_this_sprite_click_released` is not yet implemented. 

        Returns an `Event` that is triggered when the mouse click of the given sprite is released.  
        The event handler does not take in any parameter.

        Parameters
        ---
        sprite: Sprite
            The sprite on which you want the click to be detected. The removal of this sprite will lead to the removal of this event so
            it does not need to be included in `other_assoicated_sprite`
        
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        t = self._create_event(set(list(other_associated_sprites)+[sprite]))

        if not sprite in self._sprite_click_release_trigger:
            self._sprite_click_release_trigger[sprite] = []
            
        self._sprite_click_release_trigger[sprite].append(t)
        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = _declare_callback_type(t, sample_callback)
        return t

    # TODO: testing needed
    def when_backdrop_switched(self, backdrop_key: str, associated_sprites : Iterable[Sprite]=[]) -> Event[[]]:
        """
        It is recommended to use the `Sprite.when_backdrop_switched` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  

        Returns an `Event` that is triggered when the game is switched to a backdrop with the key `backdrop_key`.

        The event handler does not take in any parameter.

        Parameters
        ---
        backdrop_key: str
            The index of the backdrop  

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
                
        t = self._create_event(associated_sprites)

        if TYPE_CHECKING:
            def sample_callback()-> Any:
                return
            t = _declare_callback_type(t, sample_callback)

        self._specific_backdrop_event_emitter.add_event(backdrop_key, t)
        return t
    
    # TODO: testing needed
    def when_any_backdrop_switched(self, associated_sprites : Iterable[Sprite]=[]) -> Event[[Union[str,None]]]:
        """
        It is recommended to use the `Sprite.when_any_backdrop_switched` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  
        
        Returns an `Event` that is triggered when the backdrop is switched. 

        The event handler have to take one parameter:
        - **str** (str): The key of the new backdrop  
        
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        t = self._create_event(associated_sprites)
        self._backdrop_change_triggers.append(t)
        if TYPE_CHECKING:
            def sample_callback(key: Union[str, None])-> Any:
                return
            t = _declare_callback_type(t, sample_callback)

        return t

    def when_timer_above(self, t, associated_sprites : Iterable[Sprite]=[]) -> Condition:
        """
        It is recommended to use the `Sprite.when_timer_above` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  
        
        Returns a `Condition` that is triggered after the game have started for `t` seconds.
        A `Condition` works the same way an `Event` does. 

        The event handler have to take one parameter:
        - **n** (int): This value will always be zero

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        t = t*1000
        return self.when_condition_met(lambda:(self._current_time_ms>t), 1, associated_sprites)
    
    def when_started_as_clone(self, sprite, associated_sprites : Iterable[Sprite]=[]) -> Event[[Sprite]]:
        """
        Returns an `Event` that is triggered after the given sprite is cloned by `Sprite.create_clone`.
        Cloning of the clone will also trigger the event. 

        The event handler have to take one parameter:
        - **clone_sprite** (Sprite): The newly created clone.
                
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        
        trigger = self._create_event(associated_sprites)
        self._clone_event_manager.new_trigger(sprite, trigger)
        if TYPE_CHECKING:
            def sample_callback(clone_sprite: Sprite)-> Any:
                return
            trigger = _declare_callback_type(trigger, sample_callback)
        return trigger

    def when_receive_message(self, topic: str, associated_sprites : Iterable[Sprite]=[]) -> Event[[Any]]:
        """
        It is recommended to use the `Sprite.when_receive_message` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  

        Returns an `Event` that is triggered after a message of the given `topic` is broadcasted.

        The event handler have to take one parameter:
        - **data** (Any): This parameter can be anything passed on by the message.

        Parameters
        ---
        topic: str
            Can be any string. If the topic equals the topic of a broadcast, the event will be triggered. 
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        
        trigger = self._create_event(associated_sprites)
        self.__new_subscription(topic, trigger)
        if TYPE_CHECKING:
            def sample_callback(data: Any)-> Any:
                return
            trigger = _declare_callback_type(trigger, sample_callback)
        return trigger

    
    def broadcast_message(self, topic: str, data: Any=None):
        """
        Sends a message of a given `topic` and `data`.
        Triggers any event that subscribes to the topic. 
        The handlers of the events will receive `data` as the parameter.

        Example:
        ```python
        def event_handler(data):
            print(data) # data will be "hello world!"

        game.when_receive_message('print_message').add_handler(event_handler)
        game.broadcast_message('print_message', data='hello world!')

        # "hello world!" will be printed out
        ```
        Parameters
        ---
        topic: str
            Can be any string. If the topic of an message event equals the topic of the broadcast, the event will be triggered. 

        data: Any
            Any arbitory data that will be passed to the event handler
        
        """
        if not topic in self._all_message_subscriptions:
            return 
        
        self._all_message_subscriptions[topic] = list(filter(lambda t: t.stay_active, self._all_message_subscriptions[topic]))
        for e in self._all_message_subscriptions[topic]:
            e.trigger(data)

    def __new_subscription(self, topic: str, trigger: Event):
        if not (topic in self._all_message_subscriptions):
            self._all_message_subscriptions[topic] = []

        self._all_message_subscriptions[topic].append(trigger)

    def start_handler(self, handler:Optional[Callable[[], Any]]=None, associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE*

        It is recommended to use the `Sprite.start_handler` alias instead of this method, 
        so you don't need to specify the `associated_sprites` in every event.  

        Run the event handler immediately. Useful when creating a sprite within a function.

        The handler does not take in any parameters. 

        Parameters
        ---
        handler: Function
            A function to run. 

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        
        """
        e = self._create_event(associated_sprites)
        if handler: 
            e.add_handler(handler)
        e.trigger()
        return e


    ## advance events
    def create_pygame_event(self, types: List[int], associated_sprites : Iterable[Sprite]=[]) -> Event[[pygame.event.Event]]:
        """
        *EXTENDED FEATURE*

        Receives specific types of pygame events when they happen. 

        See pygame.event for more details: https://www.pygame.org/docs/ref/event.html

        ```python
        def key_press_event(event):
            # the event argument is a `pygame.event.Event`. 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                print("the key d is down")

            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                print("the key d is up")

        pysc.game.create_pygame_event([pygame.KEYDOWN, pygame.KEYUP])           
        ```

        The event handler have to take one parameter:
        - **event** (pygame.event.Event): An pygame event object. 

        Parameters
        ---
        types: List[int]
            A list of the pygame event flags. 

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        
        condition = self.when_condition_met(associated_sprites)
        
        def checker_hijack():
            for e in self._all_pygame_events:
                if e.type in types:
                    condition.trigger.trigger(e)

            if not condition.trigger.stay_active:
                condition.remove()

        condition.change_checker(checker_hijack)

        return cast(Event[pygame.event.Event], condition.trigger)


    def _create_specific_collision_trigger(self, sprite1: Sprite, sprite2: Sprite, other_associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        DOCUMENTATION NOT COMPLETED

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        #"""Cannot change the collision type of the object after calling this function"""
        trigger = self._create_event(set(list(other_associated_sprites)+[sprite1, sprite2]))

        self._trigger_to_collision_pairs[trigger] = sprite1, sprite2

     
        return trigger

    def _create_type2type_collision_trigger(self, type_a:int, type_b:int, collision_suppressed=False, associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE*

        DOCUMENTATION NOT COMPLETED

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """        
        
        pair = (type_a, type_b) if type_a>type_b else (type_b, type_a)

        h = self._space.add_collision_handler(*pair)
        trigger = self._create_event(associated_sprites)



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


    def _create_type_collision_trigger(self, collision_type:int , collision_suppressed=False, associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE*

        DOCUMENTATION NOT COMPLETED

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        trigger = self._create_event(associated_sprites)

        collision_allowed = not collision_suppressed
        

        if not collision_type in self._collision_type_to_trigger: 
            self._collision_type_to_trigger[collision_type] = collision_allowed, []


        self._collision_type_to_trigger[collision_type][1].append(trigger)

        return trigger

    def _suppress_type_collision(self, collision_type, collision_suppressed=True):
        """
        *EXTENDED FEATURE*

        DOCUMENTATION NOT COMPLETED

        """
        collision_allowed = not collision_suppressed

        if not collision_type in self._collision_type_to_trigger: 
            self._collision_type_to_trigger[collision_type] = collision_allowed, []    
        else:
            t_list = self._collision_type_to_trigger[collision_type][1]
            self._collision_type_to_trigger[collision_type] = collision_allowed, t_list


    def when_timer_reset(self, reset_period: Optional[float]=None, repeats: Optional[int]=None, associated_sprites: Iterable[Sprite]=[]) -> TimerCondition:
        """
        *EXTENDED FEATURE*

        Repeats an event for `repeats` time for every `reset_period` seconds. 

        ```python
        
        def print_counts(n):
            print(n) # n is the number of remaining repeats

        # every one second, for 100 times
        pysc.game.when_timer_reset(1, 100).add_handler(print_counts)

        # will start printing 99, 98, ..., 0 every 1 second. 
        ```

        The event handler have to take one parameter:
        - **n** (int): The number of remaining repeats

        Parameters
        ---
        reset_period: float
            The reset period of the timer. The handlers are triggered on timer reset. 

        repeats: int or None
            How many times to repeat. Set to None for infinite repeats. 

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        if reset_period is None: 
            reset_period = np.inf

        if repeats is None:
            _repeats = np.inf
        else:
            _repeats = repeats

        condition = TimerCondition(reset_period, _repeats)
        self._all_conditions.append(condition)
        self._all_triggers.append(condition.trigger)

        self._sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )                
        return condition
    
    
    def when_condition_met(self, checker=lambda: False,  repeats: Optional[int]=None,  associated_sprites: Iterable[Sprite]=[])-> Condition:
        """
        *EXTENDED FEATURE*

        For every frame, if a condition is met, the event is triggered. Repeated up to `repeats` times. 

        The condition is provided by a function that takes no argument and returns a boolean. 
        
        ```python
        def slowly_move_sprite_out_of_edge(n):
            my_sprite.x += 1
            
        pysc.game.when_condition_met(lambda: (my_sprite.x<0), None).add_handler(slowly_move_sprite_out_of_edge)
        ```

        The event handler have to take one parameter:
        - **n** (int): The number of remaining repeats

        Parameters
        ---
        checker: Callable[[], bool] 
            A function that takes no argument and returns a boolean. 
            The checker is run one every frame. If it returns true, the handler is called. 

        repeats: int or None
            How many times to repeat. Set to None for infinite repeats. 

                    
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """

        if repeats is None:
            _repeats = np.inf
        else:
            _repeats = repeats

        condition = Condition(checker, _repeats)
        self._all_conditions.append(condition)
        self._all_triggers.append(condition.trigger)

        self._sprite_event_dependency_manager.add_event(
            condition, associated_sprites
        )        
        return condition
    
    def when_mouse_click(self, associated_sprites: Iterable[Sprite]=[] ) -> Event[[Tuple[int, int], int, str]]:
        """
        *EXTENDED FEATURE*

        Returns an `Event` that is triggered when the mouse is clicked or released. 
        
        The event handler have to take three parameters:
        - **pos** (Tuple[int, int]): The location of the click
        - **button** (int): Indicates which button is clicked. 0 for left, 1 for middle, 2 for right and other numbers for scrolling.     
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a press or a release

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
    
        """
        event_internal = self.create_pygame_event([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN], associated_sprites)
        event = self._create_event(associated_sprites)
        def handler(e: pygame.event.Event):
            updown = "up" if e.type == pygame.MOUSEBUTTONUP else "down"
            event.trigger(e.pos, e.button, updown)
        event_internal.add_handler(handler)

        return event
    
    def when_mouse_scroll(self, associated_sprites: Iterable[Sprite]=[] ) -> Event[[str]]:
        """
        *EXTENDED FEATURE*

        Returns an `Event` that is triggered when the mouse is scrolled. 
        
        The event handler have to take one parameters:
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a scroll up or a scroll down.

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
    
        """
        event_internal = self.create_pygame_event([pygame.MOUSEWHEEL], associated_sprites)
        event = self._create_event(associated_sprites)
        def handler(e):
            updown = "up" if e.y > 0 else "down"
            event.trigger(updown)
        event_internal.add_handler(handler)

        return event
    

    def _create_event(self, associated_sprites: Iterable[Sprite]=[]) -> Event:
        """
        
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """

        trigger = Event()
        self._all_triggers.append(trigger)

        self._sprite_event_dependency_manager.add_event(
            trigger, associated_sprites
        )
        return trigger
    

game = Game()
"""
The singleton Game object. This is the object that represent the game.   
"""


def is_key_pressed(key: str) -> bool:
    """
    Returns a bool(True/False) that indicates if the given key is pressed.

    Usage
    ```python
    if is_key_pressed('space'):
        print('space pressed')
    ```
    """
    keycode = pygame.key.key_code(key)
    result = pygame.key.get_pressed()
    return result[keycode]


def get_mouse_pos() -> Tuple[int, int]:
    """
    Returns the mouse coordinate. 
    
    Usage
    ```python
    mouse_x, mouse_y = get_mouse_pos()
    ```
    """
    return pygame.mouse.get_pos()


def get_mouse_presses() -> Tuple[bool, bool, bool]:
    """
    Returns the mouse presses. 
    ```python
    is_left_click, is_middle_click, is_right_click = get_mouse_presses()
    ```
    """
    return pygame.mouse.get_pressed(num_buttons=3)

# def _is_touching(sprite_a:Sprite, sprite_b:Sprite):
#     """
#     pymunk
#     """
#     for pair in game._contact_pairs_set:

#         if (sprite_a._shape in pair) and (sprite_b._shape in pair):
#             return True
#     return False


# def _is_touching_mouse(sprite: Sprite):
#     return sprite._shape.point_query(pygame.mouse.get_pos()).distance <= 0
        