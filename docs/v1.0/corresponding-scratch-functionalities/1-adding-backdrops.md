---
title: Adding a Backdrop
parent: Corresponding Scratch Functionalities
nav_order: 1
---
# Adding a Backdrop

## 1. Find or create an image for the backdrop
Follow this [guide](../asset-preparation-guide/) to learn how to do it. 

## 2. Put the image to the asset folder
1. For an example, locate this image `my_first_game/pyscratch/example/getting-started/assets/my_background.jpg`. 

2. Copy and paste it inside this `assets` folder. 
```
├─ my_first_game/
    ├─ assets/
        ├─ my_background.jpg
```

## 3. Load the image to the game

Add these lines into `main.py` after the import

```python
# load the image into python 
background_image = pysc.helper.load_image('assets/my_background.jpg')

# pass in a list of all the available backdrops. 
pysc.game.set_backdrops([background_image])

# choose the backdrop at index 0
# analogous to the scratch block: 'switch backdrop to [backdrop0]'
pysc.game.switch_backdrop(0) 
```


Or if you have more than one backdrop:
```python
# load the image into python 
background_image = pysc.helper.load_image('assets/my_background.jpg')
background_image2 = pysc.helper.load_image('assets/my_background2.jpg')
background_image3 = pysc.helper.load_image('assets/my_background3.jpg')

# pass in a list of all the available backdrops. 
pysc.game.set_backdrops([background_image, background_image2, background_image3])

# choose the backdrop at index 0
pysc.game.switch_backdrop(0) 
```

## Optionally fit the backdrop to the screen size
```python
background_image = pysc.helper.load_image('assets/my_background.jpg')

screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
background_image = pysc.helper.scale_to_fill(background_image, screen_size)
# background_image = pysc.helper.scale_to_fit_aspect(background_image, screen_size)
# background_image = pysc.helper.scale_and_tile(background_image, screen_size)
```

## Your `main.py` should look like this
```python
import pyscratch as pysc

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

background_image = pysc.helper.load_image('assets/my_background.jpg')
# background_image = pysc.helper.scale_to_fill(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pysc.game.set_backdrops([background_image])
pysc.game.switch_backdrop(0)

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```