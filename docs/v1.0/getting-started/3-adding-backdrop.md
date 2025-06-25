---
title: Adding a Backdrop
parent: Getting Started
nav_order: 3
---
# Adding a Backdrop
---
## Find a suitable image for the backdrop
1. We have already prepared an backdrop for this tutorial. Locate this image `my_first_game/pyscratch/example/getting-started/assets/my_background.jpg`. Open it and have a look. 

2. Copy and paste it inside the `assets` folder. 

Your folder now looks like this
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ assets/
        ├─ player-fish.png
        ├─ my_background.jpg
    ├─ main.py
    ├─ player.py
```
## Reference this image in `main.py`
Adding a backdrop is as simple as just adding these three lines in `main.py` before the game start.

```python
# load the image
backdrop_img = pysc.load_image('assets/my_background.jpg') 

# a list of all the backdrop images 
pysc.game.set_backdrops([backdrop_img]) 

# use the backdrop at index 0 (use can switch the backdrop anywhere in the game)
pysc.game.switch_backdrop(0) 
```

<details markdown="block">
  <summary>
    In case you have multiple backdrops (not a part of this tutorial): 
  </summary>


```python
# load the images
backdrop_img0 = pysc.load_image('assets/my_background0.jpg') 
backdrop_img1 = pysc.load_image('assets/my_background1.jpg') 
backdrop_img2 = pysc.load_image('assets/my_background2.jpg') 

# a list of all the backdrop images 
pysc.game.set_backdrops([backdrop_img0, backdrop_img1, backdrop_img2]) 

# use the backdrop at index 0 
pysc.game.switch_backdrop(0) 
```
</details>



## Now your `main.py` look like this

<details markdown="block">
  <summary>
    main.py
  </summary>



```python
import pyscratch as pysc
import player

# backdrop
backdrop_img = pysc.load_image('assets/my_background.jpg') # load the image(s)
pysc.game.set_backdrops([backdrop_img]) # a list of all the backdrop images 
pysc.game.switch_backdrop(0) # use the backdrop at index 0 


# start the game
screen_height = 720
screen_width = 1280
framerate = 60

pysc.game.update_screen_mode((screen_width, screen_height))
pysc.game.start(framerate)
```

</details>



<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="{{ site.cdn_url }}vid/background.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>