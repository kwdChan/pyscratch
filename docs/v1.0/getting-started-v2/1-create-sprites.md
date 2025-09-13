---
title: Adding Sprites
parent: Getting Started (New)
nav_order: 1
---

# Add a sprite to the game
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


## Before creating the sprite
1. [Click here]() to download the tutorial pack. Unzip it and put it to the project folder.

2. Create an empty folder called `assets`. 

The tutorial pack contains some images that you might want to use for your game. 
Open it and have a look. 
Your project file should now look like this. 
```
├─ my_first_game/
    ├─ tutorial_pack/
        ├─ ...
    ├─ assets/
    ├─ main.py
```


## Add a sprite called player
---

### 1. Put the image to the asset folder
**Find an image you like and put it to the folder `assets`.**

This time, let's choose the `fish_brown_outline.png` inside the tutorial pack. 

Now the project folder look like this. 
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ fish_brown_outline.png
    ├─ main.py
```

### 2. Open a new file for a new sprite
In Pyscratch, each sprite should have its own python file that contains the codes controlling the sprite. This is analogous to Scratch having different tabs for different sprites. 

**We open a new file called `player.py` and put these lines in to `player.py`**. 

```python
import pyscratch as pysc

# note that you need to match the image file name! 
player = pysc.create_single_costume_sprite("assets/fish_brown_outline.png")
player.set_draggable(True) # optional: make the sprite draggable
```


Your project folder should look like this: 
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ fish_brown_outline.png
    ├─ main.py
    ├─ player.py
```





### 3. Import the sprite to `main.py` and run it

**Firstly, `main.py` is always where you start your game program**, not any sprite files like this player.py. If you just run `player.py`, **nothing will happen**.

Secondly, if you just run `main.py` as it was, you won’t see your new sprite. **You need to add `import player`** in order to tell python to include your code in player to the main program. 

And now you will see your sprite in the scene when you run `main.py`.


```python
import pyscratch as pysc
import player # Very important!

# start the game
WIN_WIDTH = 500 # change me
WIN_HEIGHT = 500 # change me
framerate = 60

pysc.game.update_screen_mode((WIN_WIDTH, WIN_HEIGHT)) 
pysc.game.start(framerate)
```


## Your turn: add another sprite to the game using any image of your choice 
---