---
title: Clone a Sprite
parent: Getting Started
nav_order: 4
---
# Clone a Sprite
{: .no_toc }
---
Let's create some other fishes to the game. 
<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Create the parent sprite

First, we create the sprite as uaual.

**1. Find a suitable image for the sprite and put in to the asset folder**     
Again, we have prepared the sprite image for this example. 

Put this image `my_first_game/pyscratch/example/getting-started/assets/kenney/other_fishes/0.png` to the asset folder and rename it to `other_fishes.png`


**2. Create a new file for the sprite**
We open a file called `enemy.py` and put these lines in. 

```python
import pyscratch as pysc
from settings import *

enemy = pysc.create_single_costume_sprite("assets/other_fishes.png")
enemy.set_draggable(True) # make the sprite draggable
```

**3. Import enemy in main.py**
```python
# change `import player` to this line:
import player, enemy

```
Now if you run `main.py`, you should be able to see the new fish. 

## Clone the sprite 
We want to clone the sprite every 2 seconds and make them appear in a somewhat random location. 

**1. Create the clones**     
```python
def clone_every_2_sec():
    while True:
        enemy.clone_myself() # analogous to `create clone of [enemy]` in scratch
        yield 2

enemy.when_game_start().add_handler(create_enemy)

# the above is the same as: 
# game_start_event = enemy.when_game_start()
# game_start_event.add_handler(create_enemy)

```

<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="create-clone.png" alt="create-clone" width="200"/>
</details>




**2. When I start as a clone**
We use the `when_started_as_clone` event to program the movement of the clone. 
This event requires a handler function that takes in a sprite as a parameter. When the clone is created, the event will call your handler function and pass in the clone sprite so you can control it. 


```python
def clone_movement(clone_sprite):

    # start the fish from the left edge at a random height
    clone_sprite.y = pysc.helper.random_number(0, SCREEN_HEIGHT)
    clone_sprite.x = 0

    # random size
    size = pysc.helper.random_number(0.8, 1.2)
    clone_sprite.set_scale(size)
    
    while True:
        
        clone_sprite.move_indir(3)

        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(clone_movement)

# the above is the same as: 
# clone_event = enemy.when_started_as_clone()
# clone_event.add_handler(clone_movement)
```
<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="clone-movement.png" alt="clone-movement" width="300"/>

  Note that in this library, the top-left corner is (x=0, y=0) and buttom-right corner is (x=1280, y=720) in this example depending your `SCREEN_WIDTH` and `SCREEN_HEIGHT`.

</details>


Note that the `enemy` variable represents only the parent sprite that we clone from, not the clone itself. If you are unsure what this means, try running this incorrect version below: 

```python
def clone_movement(clone_sprite):
    # incorrect
    enemy.y = pysc.helper.random_number(0, SCREEN_HEIGHT)
    enemy.x = 0
    
    while True:
        # incorrect
        enemy.move_indir(3)

        yield 1/FRAMERATE

enemy.when_started_as_clone().add_handler(clone_movement)
```

You will see the parent fish get moved but the clone fish does not. This behaviour cannot be achieved by Scratch.



## Your folder should look like this
{: .no_toc }

<details markdown="block">
  <summary>
    Folder Structure
  </summary>
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ my_background.jpg
        ├─ player.png
        ├─ other_fishes.png
    ├─ main.py
    ├─ settings.py
    ├─ player.py
    ├─ enemy.py
```
</details>

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
        enemy.clone_myself() 
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

```
</details>


<details markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
from settings import *
import player, enemy

background_image = pysc.helper.load_image('assets/my_background.jpg')
pysc.game.set_backdrops([background_image])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```
</details>
