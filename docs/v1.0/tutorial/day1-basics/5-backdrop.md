---
title: Backdrop
parent: Day 1 - Basics
nav_order: 5
---
# Adding a Backdrop
---

<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>


## Demo 1: Adding a backdrop
- First, put the backdrop image into the asset folder. Let say the image is `undersea_bg.png`. 
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ chatgpt-chest-open.png
        ├─ fish_red_skeleton_outline.png 
        ├─ orange_red_outline.png
        ├─ undersea_bg.png
    ├─ main.py
    ├─ chest.py
    ├─ enemy.py
    ├─ friend.py
```

- Put these lines in `main.py`
<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
from pyscratch import game
import chest, enemy, friend
       
# background

## 1. Load and resize the image if necessary 
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576)) # optional: resize the image 

## 2. Make a list of all the backdrops that will be used in the game 
backdrop_list = [bg0]
game.set_backdrops(backdrop_list) # pass the list to the game

## 3. Select the backdrop
game.switch_backdrop(0)


# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)


```






