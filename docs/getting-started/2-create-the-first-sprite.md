---
title: Create the First Sprite
parent: Getting Started
nav_order: 2
---
# Create the First Sprite
---
Let's first create the player sprite. First, you need to find an image for this sprite. 

## Find a suitable image for the sprite
1. Locate this image `my_first_game/pyscratch/example/getting-started/assets/kenney/player.png`. Open it and have a look.

2. Copy and paste it inside the `assets` folder. 


## Open a new file for a new sprite
In Pyscratch, each sprite should have its own python file that contains the codes controlling the sprite. This is analogous to Scratch having different tabs for different sprites. 

We open a new file called `player.py`
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ my_background.jpg
        ├─ player.png
    ├─ main.py
    ├─ settings.py
    ├─ player.py
```

And put these lines in to `player.py` to create a new sprite.

```python
import pyscratch as pysc
from settings import *

player = pysc.create_single_costume_sprite("assets/player.png")
player.set_draggable(True) # optional: make the sprite draggable
```

Here you created a sprite and you assigned it to a variable named `player`. To optionally make this sprite draggable, you run `player.set_draggable(True)`. 


## Import the sprite to `main.py` and run it
Firstly, `main.py` is always where you start your game program, not any sprite files like this `player.py`. If you just run `player.py`, nothing will happen. 

Secondly, if you just run `main.py` as it was, you won't see your new sprite. You need to add `import player` in order to tell python to include your code in `player` to the main program. And now you will see your sprite in the scene when you run `main.py`.


## Your `main.py` should look like this
```python
import pyscratch as pysc
from settings import *
import player

background_image = pysc.helper.load_image('assets/my_background.jpg')
pysc.game.set_backdrops([background_image])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```

