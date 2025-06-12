---
title: Using Variables
parent: Getting Started
nav_order: 5
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
Let's create a random ocean current that moves all the fishes. We need some variables that are shared across different sprites. To do that, we put the variables to `pysc.game.shared_data`, which is a dictionary. 

Add these lines in either `player.py` or `enemy.py`. Same as in Scratch, if the event is not related to the sprite, it doesn't matter where you put it. 

```python
# create the variables before the start of the game
# now these variables are accessible in any event
pysc.game.shared_data['current_x'] = 0
pysc.game.shared_data['current_y'] = 0

def ocean_current_change():
    # slowly change the current variables every 0.5 second
    while True:
        pysc.game.shared_data['current_x'] += pysc.helper.random_number(-0.1, 0.1)
        pysc.game.shared_data['current_y'] += pysc.helper.random_number(-0.1, 0.1)
        yield 0.5

# you can also do either 
# `game_start_event = player.when_game_start()` if you put this in `player.py` or
# `game_start_event = enemy.when_game_start()` if you put this in `enemy.py`
# the difference between these three is minimal.
game_start_event = pysc.game.when_game_start()
game_start_event.add_handler(ocean_current_change)

```
Now add this to `enemy.py`
```python
def ocean_current_movement(clone_sprite):
    while True:
        clone_sprite.x += pysc.game.shared_data['current_x'] 
        clone_sprite.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(ocean_current_movement)

```
And add this to `player.py`

```python
def ocean_current_movement():
    while True:
        player.x += pysc.game.shared_data['current_x'] 
        player.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

player.when_game_start().add_handler(ocean_current_movement)

```

