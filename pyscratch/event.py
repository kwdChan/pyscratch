from typing import Any, Callable, Union, override
import pygame
import pymunk
import numpy as np

class Trigger:

    def __init__(self):
        self.__triggers = []
        self.__callbacks = []
        self.__stay_active = True

    def remove(self):
        self.__stay_active = False

    @property
    def stay_active(self):
        return self.__stay_active


    def trigger(self, *args, **kwargs):
        self.__triggers.append((args, kwargs))
    
    def add_callback(self, func: Callable[..., Any]):
        self.__callbacks.append(func)

    def handle_all(self):
        while self.handle_one():
            pass
        
    def handle_one(self):
        if not len(self.__triggers): 
            return False
        
        args, kwargs = self.__triggers.pop(0)

        for cb in self.__callbacks:
            cb(*args, **kwargs)

        return True


# class OneOffTrigger:
#     def __init__(self, condition_checker: Callable[[], bool]):
#         self.condition_checker = condition_checker
#         self.callback = lambda: None
    
#     def set_callback(self, func):
#         self.callback = func
    
#     def check(self):
#         if self.condition_checker():
#             self.callback()


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
        
    def add_callback(self, callback: Callable[[str], Any]):
        self.trigger.add_callback(callback)

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
        

    def on_reset(self, callback: Callable[[str], Any]):
        self.trigger.add_callback(callback)


class Timer:
    def __init__(self, reset_period=np.inf):
        self.t0 = pygame.time.get_ticks()
        self.reset_period = reset_period
        self.n_period = 0

    def read(self):
        dt = pygame.time.get_ticks() - self.t0
        self.n_period = int(dt // self.reset_period)
        return dt % self.reset_period
    

        

        



