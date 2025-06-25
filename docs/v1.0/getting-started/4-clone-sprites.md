---
title: Cloning a Sprite
parent: Getting Started
nav_order: 4
---
# Cloning a Sprite
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

Put this folder `my_first_game/pyscratch/example/getting-started/assets/other_fishes` to the asset folder. 

Your asset folder should look like this
```
├─ assets/
    ├─ other_fishes
        ├─ 0.png
        ├─ 1.png (we aren't using it yet)
    ├─ player-fish.png
    ├─ my_background.jpg
```

**2. Create a new file for the sprite**
We open a file called `enemy.py` and put these lines in. 

```python
import pyscratch as pysc

enemy = pysc.create_single_costume_sprite("assets/other_fishes/0.png")
```

**3. Import enemy in main.py**
```python
# change `import player` to this line:
import player, enemy

```
Now if you run `main.py`, you should be able to see the new fish. 

<details open markdown="block">
  <summary>
    What you would see in the game 
  </summary>
  <img src="img/enemy-creation.png" alt="img/enemy-creation.png" width="600"/>
</details>


## Clone the sprite 
We want to clone the sprite every 2 seconds and make them appear in a somewhat random location. 

**1. Create the clones**     
```python
def clone_every_2_sec():
    enemy.hide()
    enemy.set_rotation_style_left_right()
    while True:
        enemy.create_clone() # analogous to `create clone of [enemy]` in scratch
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
  <img src="img/create-clone-v3.png" alt="img/create-clone-v3" width="200"/>
</details>




**2. When I start as a clone**

We use the `when_started_as_clone` event to program the movement of the clone. 
This event requires a handler function that takes in a sprite as a parameter. When the clone is created, the event will call your handler function and pass in the clone sprite so you can control it. An error will occur if your function does not take exactly one parameter.  


```python
def clone_movement(clone_sprite):

    screen_height = 720

    # start the fish from the left edge at a random height
    clone_sprite.y = pysc.random_number(0, screen_height)
    clone_sprite.x = 0

    # random size
    size = pysc.random_number(0.8, 1.2)
    clone_sprite.set_scale(size)

    # show the clone
    clone_sprite.show()

    while True:
        clone_sprite.move_indir(3)
        yield 1/60

enemy.when_started_as_clone().add_handler(clone_movement)

# the above is the same as: 
# clone_event = enemy.when_started_as_clone()
# clone_event.add_handler(clone_movement)
```
<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/clone-movement-v2.png" alt="img/clone-movement-v2" width="300"/>

  Note that in this library, the top-left corner is (x=0, y=0) and buttom-right corner is (x=1280, y=720) in this example (depending your window width and height).

</details>

<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>


  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="vid/clone-simple_down.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>


## Confusing the parent and the clones

Note that the `enemy` variable represents only the parent sprite that we clone from, not the clone itself. 
If you confuse the parent with the clone in the event handler, you will get this seemingly erratic behaviour:
<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>


  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="vid/clone-wrong_down.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>

<details markdown="block">
  <summary>
    The code and the explanation of the behaviour
  </summary>

```python
def clone_movement(clone_sprite):

    screen_height = 720

    # incorrectly changing the position of the parent 
    # instead of the clones
    enemy.y = pysc.random_number(0, screen_height)
    enemy.x = 0

    # random size
    size = pysc.random_number(0.8, 1.2)
    enemy.set_scale(size) # changing the size of the parent (thus the subsequent clone)

    # intended to show the clone but the parent is shown
    # since the parent is not hidden anymore, the subsequent clone aren't hidden either. 
    enemy.show()

    while True:
        
        # incorrectly moving the parent instead of the clone.
        # the result is that the parent is moved an extra 3 steps every frame every time a clone is created
        # this is why the fish (the parent) moves faster and faster
        # the clone, however, stays stationary. 
        enemy.move_indir(3)

        yield 1/60

enemy.when_started_as_clone().add_handler(clone_movement)
```

  
</details>




## Your files should look like this

<details markdown="block">
  <summary>
    Folder Structure
  </summary>
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ my_background.jpg
        ├─ player-fish.png
        ├─ other_fishes/
    ├─ main.py
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


# create the sprite
enemy = pysc.create_single_costume_sprite("assets/other_fishes/0.png")

# Event: when_game_start, clone creation
def enemy_on_game_start():
    enemy.set_rotation_style_left_right()
    enemy.hide() # hide the parent

    # clone itself very 2 seconds
    while True: 
        enemy.create_clone()
        yield 2

enemy.when_game_start().add_handler(enemy_on_game_start)


# Event: when_started_as_clone, clone movement
def clone_movement(clone_sprite):

    screen_height = 720

    # start the fish from the left edge at a random height
    clone_sprite.y = pysc.random_number(0, screen_height)
    clone_sprite.x = 0

    # random size
    size = pysc.random_number(0.8, 1.2)
    clone_sprite.set_scale(size)

    # show the clone
    clone_sprite.show()

    while True:
        
        clone_sprite.move_indir(3)

        yield 1/60

enemy.when_started_as_clone().add_handler(clone_movement)
```
</details>

## Polish the game a little bit more
Update `enemy.py` so 
1. the other fishes come from either the left or right
2. the fishes don't go in a completely straight line

See `my_first_game/pyscratch/example/getting-started/step 4 - clone a sprite` for the code. 

See [getting-started](index.md#optional-run-each-step-of-this-tutorial-in-your-own-computer) to run this step in your own computer.

<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>

  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="vid/clone-sprite.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>