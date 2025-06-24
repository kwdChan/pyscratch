---
title: Create the First Sprite
parent: Getting Started
nav_order: 1
---
# Create the First Sprite
---
Let's first create the player sprite. First, you need to find an image for this sprite. 

## Find a suitable image for the sprite
1. Create a new folder called `assets`. All the media, including images, sound and fonts will be put inside this folder. 

2. We have already prepared a sprite image for this tutorial. Locate this image `my_first_game/pyscratch/example/getting-started/assets/player-fish.png`. Open it and have a look.

3. Copy and paste it inside the `assets` folder. 

Assuming that you have already created the empty scene following the [previous page](index), now your folder should look like this. 

## Open a new file for a new sprite
In Pyscratch, each sprite should have its own python file that contains the codes controlling the sprite. This is analogous to Scratch having different tabs for different sprites. 

We open a new file called `player.py`
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ player-fish.png
    ├─ main.py
    ├─ player.py
```

And put these lines in to `player.py` to create a new sprite.

```python
import pyscratch as pysc


player = pysc.create_single_costume_sprite("assets/player-fish.png")
player.set_draggable(True) # optional: make the sprite draggable
```

Here you created a sprite and you assigned it to a variable named `player`. To optionally make this sprite draggable, you run `player.set_draggable(True)`. 


## Import the sprite to `main.py` and run it
Firstly, `main.py` is always where you start your game program, not any sprite files like this `player.py`. If you just run `player.py`, nothing will happen. 

Secondly, if you just run `main.py` as it was, you won't see your new sprite. You need to add `import player` in order to tell python to include your code in `player` to the main program. And now you will see your sprite in the scene when you run `main.py`.


## Your `main.py` should look like this
<details markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
import player

# start the game
screen_height = 720
screen_width = 1280
framerate = 60

pysc.game.update_screen_mode((screen_width, screen_height))
pysc.game.start(framerate)
```

</details>