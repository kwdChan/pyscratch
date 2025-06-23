---
title: Using Variables
parent: Getting Started
nav_order: 5
---
# Using Variables
{: .no_toc }

---
Unlike Scratch, there are various ways to create variables in pyscratch. I will walk you through two of them in this section. 

<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

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

player.when_game_start().add_handler(movement)

```
Note that the variables defined inside the function is not accessible outside the function. 

<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/movement-drift.png" alt="img/movement-drift" width="300"/>
</details>


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
# `player.when_game_start()` if you put this in `player.py` or
# `enemy.when_game_start()` if you put this in `enemy.py`
# the difference between these three is minimal.
pysc.game.when_game_start().add_handler(ocean_current_change)
```
<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/current-changes.png" alt="img/current-changes" width="300"/>
</details>




Now add this to `enemy.py`
```python
def ocean_current_movement(clone_sprite):
    while True:
        clone_sprite.x += pysc.game.shared_data['current_x'] 
        clone_sprite.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(ocean_current_movement)
```
<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/moved-by-current-clone.png" alt="img/moved-by-current-clone" width="200"/>
</details>



And add this to `player.py`

```python
def ocean_current_movement():
    while True:
        player.x += pysc.game.shared_data['current_x'] 
        player.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

player.when_game_start().add_handler(ocean_current_movement)

```
<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/moved-by-current.png" alt="img/moved-by-current" width="200"/>
</details>



## Your files should look like this

<details markdown="block">
  <summary>
    enemy.py
  </summary>

```python
import pyscratch as pysc
from settings import *

# create the parent sprite
enemy = pysc.create_single_costume_sprite("assets/other_fishes.png")

## event: when game start -> create the clone
def clone_every_2_sec():
    while True:
        enemy.create_clone() 
        yield 2

enemy.when_game_start().add_handler(create_enemy)

## event: when started as clone -> movement
def clone_movement(clone_sprite):

    clone_sprite.y = pysc.helper.random_number(0, SCREEN_HEIGHT)
    clone_sprite.x = 0

    size = pysc.helper.random_number(0.8, 1.2)
    clone_sprite.set_scale(size)
    
    while True:
        clone_sprite.move_indir(3)

        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(clone_movement)

## event: when started as clone -> movement by current
def ocean_current_movement(clone_sprite):
    while True:
        clone_sprite.x += pysc.game.shared_data['current_x'] 
        clone_sprite.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(ocean_current_movement)
```
</details>


<details markdown="block">
  <summary>
    player.py
  </summary>

```python
import pyscratch as pysc
from settings import *

player = pysc.create_single_costume_sprite("assets/player.png")
player.set_draggable(True) # optional: make the sprite draggable

# event: when game started -> movement 
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

player.when_game_start().add_handler(movement)


def ocean_current_movement():
    while True:
        player.x += pysc.game.shared_data['current_x'] 
        player.y += pysc.game.shared_data['current_y'] 
        yield 1/FRAMERATE

player.when_game_start().add_handler(ocean_current_movement)
```
</details>
