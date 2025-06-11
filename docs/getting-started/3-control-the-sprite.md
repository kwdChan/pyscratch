---
title: Control the Sprite
parent: Getting Started
nav_order: 3
---
# Control the Sprite
If you are working in Scratch, you would have your sprite created by now and you would be programming the behaviour of the sprite using the code blocks. This is what we are going to do now in Python. 

We want the movement of the player using the wasd keys. In Scratch, you will have a forever loop, triggered by the "when green flag clicked" event, testing if the keys are pressed. We will do the same in Python here. 

```python
def movement():
    # analogous to the motion block: 'set rotation style [left-right]'
    player.set_rotation_style_left_right()

    # analogous to the control block: forever
    while True:

        # analogous to the control block: 'if'
        # analogous to the sensing block: 'key [w] pressed'
        if pysc.sensing.is_key_pressed('w'):
            
            # analogous to the motion block: change y by [-4]
            player.y -= 4 

        if pysc.sensing.is_key_pressed('s'):

            # analogous to the motion block: change y by [4]
            player.y += 4

        if pysc.sensing.is_key_pressed('a'):

            # analogous to the motion block: point in direction [180]
            # 180 is pointing to the left; 0 is pointing to the right
            player.direction = 180
            player.x -= 4
            
        if pysc.sensing.is_key_pressed('d'):
            player.direction = 0
            player.x += 4


        # since we had FRAMERATE = 60; 
        # this is analogous to the control block: wait [1/60] seconds
        # basically wait for one frame
        yield 1/FRAMERATE  
        
        # unlike scratch, the wait here is necessary. Without waiting here, python will put everything aside to attempt to run the loop as quickly as possible and thus halt everything else in the program.


# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_handler(movement)
```

A function in python is similar to the stack of code blocks without the event on top (without the event on top, the code blocks will never run); and passing the function to the event as the handler is essentially attaching the stack of code blocks to the event block in Scratch. 


## How do I know what functions to use? How does these functions work? 
This library is designed to be highly analogous to Scratch, and most of the Scratch blocks that you are familiar with has a corresponding Python function. All of these functions are listed and explained [here](../corresponding-scratch-blocks/). 



## Now your `player.py` look like this
```python
def movement():
    player.set_rotation_style_left_right()

    while True:
        if pysc.sensing.is_key_pressed('w'): 
            player.y -= 4

        if pysc.sensing.is_key_pressed('s'):
            player.y += 4

        if pysc.sensing.is_key_pressed('a'):
            player.direction = 180
            player.x -= 4
            
        if pysc.sensing.is_key_pressed('d'):
            player.direction = 0
            player.x += 4

        # wait for one frame
        yield 1/FRAMERATE
    
# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_handler(movement)
```