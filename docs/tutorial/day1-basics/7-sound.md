---
title: 7. Sound
parent: Day 1 - Basics
nav_order: 7 
---

# 7. Adding a Sound
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


## Demo 1: Loading the Sounds
**1. Add these two sound files `Circus-Theme-Entry-of-the-Gladiators-Ragtime-Version(chosic.com).mp3` and `impactMetal_light_004.ogg` into the asset folder**
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ chest-open.png
        ├─ fish_red_skeleton_outline.png 
        ├─ orange_red_outline.png
        ├─ undersea_bg.png
        ├─ Cat In Space Wallpaper Hq.jpg
        ├─ Circus-Theme-Entry-of-the-Gladiators-Ragtime-Version(chosic.com).mp3
        ├─ impactMetal_light_004.ogg
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
       
# sound
game.load_sound("hit", "assets/impactMetal_light_004.ogg")
game.load_sound("background", "assets/Circus-Theme-Entry-of-the-Gladiators-Ragtime-Version(chosic.com).mp3")

# backdrops
... 
# starting the game
...
```
</details>


Now you can play the sound by the name. 

## Demo 2: Play a sound effect when the enemy fish is clicked

Use `game.play_sound("hit")` to play the sound. 

<details open markdown="block">
  <summary>
    enemy.py
  </summary>

```python
@enemy.when_this_sprite_clicked()
def play_sound_when_clicked():
    """
    when_this_sprite_clicked:
    play a sound
    """
    game.play_sound("hit")
```
</details>



## Demo 3: Playing Background Music 
We want to play the sound track repeatedly when it finishes. 
Since the sound track is 2 minutes and 31 seconds long, we wait for 2*60+31 seconds plus an extra 2 seconds for a break.  

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python

# background music
@game.when_game_start()
def play_loop():
    """
    when_game_start:
    Continuously play the background music 
    """
    while True:
        game.play_sound("background", volume=0.3)
        yield 2*60+31 + 2 # or you can just put 153 

# starting the game
...
```
</details>



<details open markdown="block">
  <summary>
    The game with music on
  </summary>
  <video controls loop playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/6-1.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>

{: .text-right}
[Next Step](./8-summary){: .btn .btn-purple }

