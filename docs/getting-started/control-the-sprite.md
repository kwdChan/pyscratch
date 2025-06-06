---
title: Control the Sprite
parent: Getting Started
nav_order: 2
---
# Control the Sprite
If you are working in Scratch, you would have your sprite created by now you would be programming the behaviour of the sprite using the code blocks. This is what we are going to do in Python. 


We want the left paddle to move up when the 'w' key is down, and to move down when the 's' key is down. 

In Scratch, you will have a forever loop, triggered by the "when green flag clicked" event, testing if the keys are pressed. In Python, we create the loop first and then pass it on to the event. 

```python
def movement():

    # This is a forever loop
    while True: 
        
        if pysc.sensing.is_key_pressed('w'):
            sprite.y -= 8

        if pysc.sensing.is_key_pressed('s'):
            sprite.y += 8

        # wait for one frame (1/60th of a second)
        # can go lower or higher. doesn't really matter. 
        yield 1/60
    
        # used the keyword yield to wait for a certain time. 
        # for example, yield 1 means wait for 1 second 

        # without the waiting here, python will put everything aside to attempt to run the loop as quickly as possible and thus halt everything else in the program. yield 0 has no effect. 



game_start_event = sprite.when_game_start()
game_start_event.add_callback(movement)

```


In scratch, every stack of code blocks start from an event. An event happens, and the event triggers the code to start running. Without the event on the top, the code blocks will never run.

