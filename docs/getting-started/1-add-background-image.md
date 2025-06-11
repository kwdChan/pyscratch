---
title: Add the Background Image
parent: Getting Started
nav_order: 1
---
# Add the Background Image
---
A plain grey scene is a bit bland. Let's add a background in. 

## Create a new folder for all the images and sound
1. Create a new folder called `assets`. All the media, including images, sound and fonts will be put inside this folder. 

2. Locate this image `my_first_game/pyscratch/example/getting-started/assets/vecteezy/my_background.jpg`. Open it and have a look. 

3. Copy and paste it inside this `assets` folder. 


Assuming that you have already created the empty scene following the [previous page](index), now your folder should look like this. 

```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ my_background.jpg
    ├─ main.py
    ├─ settings.py
```


## Load the image to the game

Add these three lines into `main.py` after the imports

```python
# load the image into python 
background_image = pysc.helper.load_image('assets/my_background.jpg')

# pass in a list of all the available backdrops. 
pysc.game.set_backdrops([background_image])

# choose the backdrop at index 0
# analogous to the scratch block: 'switch backdrop to [backdrop1]'
pysc.game.switch_backdrop(0) 
```


## Your `main.py` should look like this
```python
import pyscratch as pysc
from settings import *

background_image = pysc.helper.load_image('assets/my_background.jpg')
pysc.game.set_backdrops([background_image])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```