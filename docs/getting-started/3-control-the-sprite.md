---
title: Control the Sprite
parent: Getting Started
nav_order: 3
---
# Control the Sprite
If you are working in Scratch, you would have your sprite created by now and you would be programming the behaviour of the sprite using the code blocks. This is what we are going to do now in Python. 

We want the movement of the player using the wasd keys. In Scratch, you will have a forever loop, triggered by the "when green flag clicked" event, testing if the keys are pressed. We will do the same in Python here. 

```python
player.set_rotation_style_left_right()
def movement():
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


        # wait for one frame (1/60th of a second)
        # can go lower or higher. doesn't really matter. 
        yield 1/FRAMERATE
    
        # used the keyword yield to wait for a certain time. 
        # for example, yield 1 means wait for 1 second 

        # without the waiting here, python will put everything aside to attempt to run the loop as quickly as possible and thus halt everything else in the program. yield 0 has no effect. 


# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_callback(movement)


```

A function in python is similar to the stack of code blocks without the event on top (without the event on top, the code blocks will never run); and passing the function to the event as the handler is essentially attaching the stack of code blocks to the event block in Scratch. 



## How do I know what functions to use? How does these functions work? 
This library is designed to be highly analogous to Scratch, and most of the Scratch blocks that you are familiar with has a corresponding Python function. All of these functions are listed and explained [here](../corresponding-scratch-blocks/). 
