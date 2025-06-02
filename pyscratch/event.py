from typing import Any, Callable, Dict, Generator, List, Set, Tuple, Union, override
from types import GeneratorType, NoneType

import pygame
import pymunk
import numpy as np

from pyscratch.scratch_sprite import ScratchSprite

class Trigger:

    def __init__(self):
        self.__triggers = []
        self.__callbacks: List[Callable[..., Union[NoneType, Generator[float]]]] = []
        self.__stay_active = True
        self.__generators: Dict[GeneratorType, float] = {}
        
    def remove(self):
        self.__stay_active = False

    @property
    def stay_active(self):
        return self.__stay_active


    def trigger(self, *args, **kwargs):
        self.__triggers.append((args, kwargs))
    
    def add_callback(self, func: Callable[..., Union[NoneType, Generator[float, None, None]]]):
        self.__callbacks.append(func)
        return self

    def handle_all(self, current_t_ms):
        while self.handle_one(current_t_ms):
            pass
        
    def handle_one(self, current_t_ms):
        if not len(self.__triggers): 
            return False
        
        args, kwargs = self.__triggers.pop(0)

        for cb in self.__callbacks:
            ret = cb(*args, **kwargs)
            if isinstance(ret, GeneratorType):

                # just to schedule to run immediately 
                # actually run when self.generators_proceed is called
                self.__generators[ret] = current_t_ms

        return True
    
    def generators_proceed(self, current_t_ms):
        # cannot have yield 0
        to_remove = []

        for g, t in self.__generators.items():
            next_t = t
            while next_t<=current_t_ms:
                try:
                    next_t = next_t+next(g)
                    self.__generators[g] = next_t
                except StopIteration:
                    next_t = np.inf
                    to_remove.append(g)

        self.__generators = {g:t for g, t in self.__generators.items() if not g in to_remove}



class ConditionInterface:
    def check(self):
        pass
    
    def remove(self):
        pass

    @property
    def stay_active(self) -> bool:
        return True

class Condition(ConditionInterface):
    def __init__(self, checker: Callable[[], bool] = lambda: False, repeats: Union[float, int]=1):
        self.trigger = Trigger()
        self.repeat_remains = repeats
        self.checker = checker
        self.__stay_active = True

    def remove(self):
        self.__stay_active = False
        self.trigger.remove()

    @property
    def stay_active(self):
        return self.__stay_active

    @override
    def check(self):
        if self.checker() and self.repeat_remains:
            self.repeat_remains -= 1
            self.trigger.trigger(self.repeat_remains)

        if not self.repeat_remains:
            self.remove()
        
    def add_callback(self, callback: Callable[[int], Any]):
        self.trigger.add_callback(callback)
        return self

    def change_checker(self, checker= lambda: False):
        self.checker = checker

    

class TimerCondition(ConditionInterface):
    def __init__(self, reset_period=np.inf, repeats=np.inf):
        self.trigger = Trigger()
        self.repeat_remains = repeats
        self.timer = Timer(reset_period=reset_period)
        self.period = 0
        self.__stay_active = True

    def remove(self):
        self.__stay_active = False
        self.trigger.remove()

    @property
    def stay_active(self):
        return self.__stay_active

    @override
    def check(self):
        self.timer.read()
        while (self.timer.n_period > self.period) and self.repeat_remains:
            self.period += 1
            self.repeat_remains -= 1
            self.trigger.trigger(self.repeat_remains)

        if not self.repeat_remains:
            self.remove()
        

    def add_callback(self, callback: Callable[[int], Any]):
        self.trigger.add_callback(callback)
        return self


class Timer:
    def __init__(self, reset_period=np.inf):
        self.t0 = pygame.time.get_ticks()
        self.reset_period = reset_period
        self.n_period = 0

    def read(self):
        dt = pygame.time.get_ticks() - self.t0
        self.n_period = int(dt // self.reset_period)
        return dt % self.reset_period
    
    def reset(self):
        self.n_period = 0
        self.t0 = pygame.time.get_ticks()

    

        

        



