"""
Everything in this module is directly under the pyscratch namespace. 
For example, instead of doing `pysc.event.Timer`,
you can also directly do `pysc.Timer`.
"""

from __future__ import annotations
from typing import Any, Callable, Dict, Generator, Generic, List, ParamSpec, Set, Tuple, TypeVar, Union, override
from types import GeneratorType, NoneType

import pygame
import pymunk
import numpy as np

P = ParamSpec('P')
"""@private"""
T = TypeVar('T')
"""@private"""


def _declare_callback_type(obj: Event, func: Callable[P, Union[NoneType, Generator[float, None, None]]]) -> Event[P]:
    return obj


class Event(Generic[P]):
    """
    A low level Event class. 
    You **do not** need to create the Event object yourself. 
    They are instead returned by functions like `sprite.when_game_started()`

    In no circumstances will you need to create your custom event. Always use the message event instead. 
    """

    def __init__(self):
        """@private"""
        
        self.__triggers: List = []
        self.__callbacks: List[Callable[P, Union[NoneType, Generator[float, None, None]]]] = []
        self.__stay_active = True
        self.__to_soft_remove = False
        self.__generators: Dict[GeneratorType, float] = {}
        

    #def add_handler(self, func: Callable[P, Union[NoneType, Generator[float, None, None]]]): 
    # use Any for the simplicity in the doc
    def add_handler(self, func: Callable[P, Any]):
        """
        Add a handler function to this event. 
        When the event is triggered, the handler functions are called, taking in the parameters passed on by the triggers.
        """
        self.__callbacks.append(func)
        return self


    def remove(self):
        """Schedule this event to be removed."""
        self.__stay_active = False

    def soft_remove(self):
        """Schedule this event to be removed when all the generators (yield functions) finish"""
        self.__to_soft_remove = True

    @property
    def stay_active(self) -> bool:
        """Shows whether this event is removed or scheduled to be removed."""
        return self.__stay_active
    


    def trigger(self, *args: P.args, **kwargs: P.kwargs):
        """
        @private
        Trigger the event. The parameters will be passed on to the event handlers.

        You will not need to run this method ever.
        """
        self.__triggers.append((args, kwargs))
    
    def _handle_all(self, current_t_ms):
        while self._handle_one(current_t_ms):
            pass
        
    def _handle_one(self, current_t_ms):

        if not len(self.__triggers): 
            return False
        
        args, kwargs = self.__triggers.pop(0)

        for cb in self.__callbacks:
            ret = cb(*args, **kwargs) # type: ignore
            if isinstance(ret, GeneratorType):

                # just to schedule to run immediately 
                # actually run when self.generators_proceed is called
                self.__generators[ret] = current_t_ms

        return True
    
    def _generators_proceed(self, current_t_ms):
        to_remove = []

        for g, t in self.__generators.items():
            next_t = t
            while next_t<=current_t_ms:
                try:
                    next_t = next_t+next(g)*1000
                    self.__generators[g] = next_t
                except StopIteration:
                    next_t = np.inf
                    to_remove.append(g)

        self.__generators = {g:t for g, t in self.__generators.items() if not g in to_remove}
        if not len(self.__generators) and self.__to_soft_remove:
            self.remove()
            



class _ConditionInterface:
    """
    A low level Condition class. 
    You **do not** need to create the Condition object yourself. 
    """
    def _check(self):
        pass

    def add_handler(self, callback: Callable[[int], Any]):
        """
        Add a handler function to this event. 
        When the event is triggered, the handler functions are called, taking in the parameters passed on by the triggers.
        """        
        return self
        
    def remove(self):
        """Schedule this event to be removed."""
        pass

    def soft_remove(self):
        """Schedule this event to be removed when all the generators (yield functions) finish"""
        pass

    @property
    def stay_active(self) -> bool:
        """Shows whether this event is removed or scheduled to be removed."""
        return True

class Condition(_ConditionInterface):
    def __init__(self, checker: Callable[[], bool] = lambda: False, repeats: Union[float, int]=1):
        """@private"""
        self.trigger = Event()
        self.repeat_remains = repeats
        self.checker = checker
        self.__stay_active = True

    def add_handler(self, callback: Callable[[int], Any]):       
        self.trigger.add_handler(callback)
        return self
    
    def remove(self):
        self.__stay_active = False
        self.trigger.remove()

    def soft_remove(self):
        self.__stay_active = False
        self.trigger.soft_remove()

    @property
    def stay_active(self):
        return self.__stay_active

    def _check(self):
        if self.checker() and self.repeat_remains:
            self.repeat_remains -= 1
            self.trigger.trigger(self.repeat_remains)

        if not self.repeat_remains:
            self.soft_remove()

    def change_checker(self, checker= lambda: False):
        """@private"""
        self.checker = checker

    

class TimerCondition(_ConditionInterface):
    def __init__(self, reset_period=np.inf, repeats=np.inf):
        """
        @private
        """
        self.trigger = Event()
        self.repeat_remains = repeats
        self.timer = Timer(reset_period=reset_period)
        self.period = 0
        self.__stay_active = True

    def add_handler(self, callback: Callable[[int], Any]):
        self.trigger.add_handler(callback)
        return self

    def remove(self):
        self.__stay_active = False
        self.trigger.remove()

    def soft_remove(self):
        self.__stay_active = False
        self.trigger.soft_remove()

    @property
    def stay_active(self):
        return self.__stay_active

    def _check(self):
        self.timer.read()
        while (self.timer.n_period > self.period) and self.repeat_remains:
            self.period += 1
            self.repeat_remains -= 1
            self.trigger.trigger(self.repeat_remains)

        if not self.repeat_remains:
            self.soft_remove()
        


class Timer:
    """
    Create a timer that resets every `reset_period` seconds. 
    """
    def __init__(self, reset_period=np.inf):
        """
        Parameters
        ---
        reset_period: float
            The reset period. Pass in np.inf for no reset
        """
        self._t0 = pygame.time.get_ticks()/1000
        self.reset_period = reset_period
        self.n_period = 0
        """How many times the `reset_period` have passed"""

    def read(self):
        """
        Read the timer.
        """
        dt = pygame.time.get_ticks()/1000 - self._t0
        self.n_period = int(dt // self.reset_period)
        return dt % self.reset_period
    
    def full_reset(self):
        """
        Reset the timer and the `n_period`.
        """
        self.n_period = 0
        self._t0 = pygame.time.get_ticks()/1000

    

        

        



