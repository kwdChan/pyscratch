---
title: 6. Backdrop
parent: Day 1 - Basics
nav_order: 6
---
# 6. Adding a Backdrop
{: .no_toc }

---

<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

{: .highlight}
> Please update PyScratch to make sure the version is at least 2.0.


## Demo 1: Adding a Backdrop
**1. Put the backdrop image into the asset folder**

Let say the image is `undersea_bg.png`
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ chest-open.png
        ├─ fish_red_skeleton_outline.png 
        ├─ orange_red_outline.png
        ├─ undersea_bg.png
    ├─ main.py
    ├─ chest.py
    ├─ enemy.py
    ├─ friend.py
```

**2. Put these lines in `main.py`**
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

## 2. Resize the image (optional)
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576))

## 3. Add the backdrop with a name
game.add_backdrop("sea", bg0) 

## 4. Select the backdrop
game.switch_backdrop("sea")


# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)
```
</details>

## Demo 2.1: Adding Multiple Backdrops 

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
# background
## Backdrop 1: sea
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576)) # optional: resize the image 
game.add_backdrop("sea", bg0) 

## Backdrop 2: lose (remember to add the image to the asset folder)
bg1 = pysc.load_image("assets/Cat In Space Wallpaper Hq.jpg")
bg1 = pysc.scale_to_fit_aspect(bg1, (1024, 576)) # optional: resize the image 
game.add_backdrop("lose", bg1) 

## 3. Select the starting backdrop
game.switch_backdrop("sea")
```
</details>


## Demo 2.2: Switching Backdrops
Use `game.switch_backdrop` anywhere in the game to change the backdrop. 

Put this event before the game start or in any sprite file. 

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
@game.when_game_start()
def background():
    """
    when_game_start: 
    if the score goes below zero, switch the backdrop to "lose"
    """
    while True:
        yield 1/game.framerate
        if game['score'] < 0: 
            game.switch_backdrop('lose')

# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)
```
</details>


##  Demo 3: Event `when_backdrop_switched`
Make the chest disappear when the backdrop is switched to `"lose"`. 

<details open markdown="block">
  <summary>
    chest.py
  </summary>

```python
@chest.when_backdrop_switched("lose")
def disappear_when_lose():
    """
    when_backdrop_switched("lose"): 
    disappear
    """
    chest.hide()
```
</details>


<details open markdown="block">
  <summary>
    After making the friend and enemy sprite disappear after the backdrop switch

  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/5-1.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>


{: .text-right}
[Next Step](./6-sound){: .btn .btn-purple }

