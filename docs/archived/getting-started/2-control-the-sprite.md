---
title: Control the Sprite
parent: Getting Started
nav_order: 2
---
# Control the Sprite
---
If you are working in Scratch, you would have your sprite created by now and you would be programming the behaviour of the sprite using the code blocks. This is what we are going to do now in Python. 

## Scratch-like Event-based Code
We want the movement of the player using the wasd keys. In Scratch, you will have a forever loop, triggered by the "when green flag clicked" event, testing if the keys are pressed. We will do the same in Python here. 

```python
# free to use any function name
def on_game_start():

    player.set_rotation_style_left_right() # analogous to the motion block: 'set rotation style [left-right]'
    while True:
        if pysc.is_key_pressed('w'): # analogous to the sensing block: 'key [w] pressed'
            player.y -= 4  # analogous to the motion block: change y by [-4]

        if pysc.is_key_pressed('s'):
            player.y += 4

        if pysc.is_key_pressed('a'):
            player.direction = 180  # analogous to the motion block: point in direction [180]
            player.x -= 4
            
        if pysc.is_key_pressed('d'):
            player.direction = 0
            player.x += 4

        # this is analogous to the control block: wait [1/60] seconds
        # because the frame rate is 60, this is basically to wait for one frame
        yield 1/60 

# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)
```
A function in python is similar to the stack of code blocks without the event on top (without the event on top, the code blocks will never run); and passing the function to the event as the handler is essentially attaching the stack of code blocks to the event block in Scratch. 

In this library, we use `yield` as as the wait block in Scratch. For example, `yield 1` means wait for one second. **Unlike Scratch, the wait is necessary within the loop.** Without waiting, python will put everything aside 
to attempt to run the loop as quickly as possible. A repeat loop (a `for` loop) for 100 times will be finished instantly, but **a forever loop without waiting will halt the program.** 

Here we wait for 1/60th of a second, which is the duration of one frame when the framerate is 60, so the movement appears smoothly. However, the choice of this value is arbitrary. You can do 1/30, 1/120, 0.01 or whatever. 

Note that in this library, 180 is pointing to the left; 0 is pointing to the right. The top-left corner is (x=0, y=0) and the buttom-right corner is (x=1280, y=720) in this example (depending your window width and window height).


<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="{{ site.cdn_url }}img/basic-movement.png" alt="img/basic-movement.png" width="300"/>
  
</details>


## How do I know what functions to use? How does these functions work? 
This library is designed to be highly analogous to Scratch, and most of the Scratch blocks that you are familiar with has a corresponding Python function. All of these functions are listed and explained [here](../corresponding-scratch-functionalities/). 


## Now your `player.py` look like this

<details markdown="block">
  <summary>
    player.py
  </summary>



```python
import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")

# free to use any function name
def on_game_start():

    player.set_rotation_style_left_right() # analogous to the motion block: 'set rotation style [left-right]'
    while True:
        if pysc.is_key_pressed('w'): # analogous to the sensing block: 'key [w] pressed'
            player.y -= 4  # analogous to the motion block: change y by [-4]

        if pysc.is_key_pressed('s'):
            player.y += 4

        if pysc.is_key_pressed('a'):
            player.direction = 180  # analogous to the motion block: point in direction [180]
            player.x -= 4
            
        if pysc.is_key_pressed('d'):
            player.direction = 0
            player.x += 4

        yield 1/60 

        
# passing the function to the event as the event handler
game_start_event = player.when_game_start()
game_start_event.add_handler(on_game_start)

# or shorter: 
# player.when_game_start().add_handler(on_game_start)


```

</details>
<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="{{ site.cdn_url }}vid/controlling.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>