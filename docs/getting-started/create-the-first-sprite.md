---
title: Create the First Sprite
parent: Getting Started
nav_order: 1
---
# Create the First Sprite
---
In Pyscratch, each sprite should have its own python file that contains the codes controlling the sprite. This is analogous to Scratch having different tabs for different sprites.   

## Open a new file for a new sprite
Remember that we are creating a pong game. So let's first create the left paddle. We open a new file called `left_paddle.py`

Assuming that you have already created the empty scene following the [previous page](index), now you have these files in the folder. 
```
├─ my_first_game
    ├─ pyscratch
    ├─ main.py
    ├─ left_paddle.py
```

And put these lines in to create a new rectangle sprite.
```python
import pyscratch as pysc

paddle_colour = (200, 200, 200)
paddle_width = 20
paddle_height = 130

sprite = pysc.create_rect_sprite(paddle_colour, paddle_width, paddle_height)
sprite.set_draggable(True)
```
This time we used `pysc.create_rect_sprite` to create the sprite. The other optional creating new sprites are listed [here](/pyscratch/assets-processing-functions/)

## Import the sprite to `main.py` and run it
Firstly, `main.py` is always where you start your game program, not any sprite files like this `left_paddle.py`. If you just run `left_paddle.py`, nothing will happen. 

Secondly, if you just run `main.py` as it was, you won't see your new sprite. You need to add `import left_paddle` in order to tell python to include your code in `left_paddle` to the main program. 

Your `main.py` should look like this. 
```python

import pyscratch as pysc
import left_paddle

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```

And now you will see your sprite in the scene when you run `main.py`.