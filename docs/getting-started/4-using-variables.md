---
title: Using Variables
parent: Getting Started
nav_order: 4

---
# Using Variables
---
Unlike Scratch, there are various ways to create variables in pyscratch. I will walk you through two of them in this section. 

## Local Variables
Let say we want our sprite to drift a little bit after we release the key instead of stopping immediately. We will need a speed variable in the x and in the y directions. We set the speed to 4 when the key is down, and we reduce the speed gradually if the key is released. 

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
        yield 1/FRAMERATE 

game_start_event = player.when_game_start()
game_start_event.add_handler(movement)

```

This is the analogous scratch code: 


<img src="movement-drift.png" alt="movement-drift.png" width="300"/>


Unlike Scratch, the variables defined inside the function is not accessible outside the function. 

## Shared Variables
