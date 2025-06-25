---
title: Local Variables
parent: Getting Started
nav_order: 5
---
# Local Variables

Let say we want our sprite to drift a little bit after we release the key instead of stopping immediately. We will need a speed variable in the x and in the y directions. We set the speed to the maximum when the key is down, and we reduce the speed gradually when the key is released. 

```python 
def movement():
    player.set_rotation_style_left_right()

    speed_y = 0
    speed_x = 0

    while True:

        if pysc.sensing.is_key_pressed('w'):
            speed_y = -4

        elif pysc.sensing.is_key_pressed('s'):
            speed_y = 4

        else:
            # reduce the speed if neither up nor down was pressed
            speed_y = speed_y*0.9

        if pysc.sensing.is_key_pressed('a'):
            player.direction = 180
            speed_x = -4
            
        elif pysc.sensing.is_key_pressed('d'):
            player.direction = 0
            speed_x = 4
        else:
            speed_x = speed_x*0.9

        # actually move the sprite
        player.y += speed_y
        player.x += speed_x

        # wait for one frame
        yield 1/60 

player.when_game_start().add_handler(movement)

```
Note that the variables defined inside the function is not accessible outside the function. 

<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="{{ site.cdn_url }}img/movement-drift.png" alt="img/movement-drift" width="300"/>
</details>

<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="{{ site.cdn_url }}vid/local-variable_down.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>


