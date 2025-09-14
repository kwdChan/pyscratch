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
Now we are ready to add new sprites in. 

## 1. Put the sprite image to the asset folder
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

## 2. Open a new file for the sprite
In Pyscratch, each sprite should have its own python file that contains the codes controlling the sprite. This is analogous to Scratch having different tabs for different sprites. 

**We open a new file called `player.py`, put these lines in, and then save it**.

<details open markdown="block">
  <summary>
    player.py
  </summary>

```python
import pyscratch as pysc

# This is the line that create the sprite. Note that you need to match the image file name! 
player = pysc.create_single_costume_sprite("assets/fish_brown_outline.png")
player.set_draggable(True) # optional: make the sprite draggable
```
</details>

<details open markdown="block">
  <summary>
    Project Folder
  </summary>

```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ fish_brown_outline.png
    ├─ main.py
    ├─ player.py
```

</details>



## 3. Import the sprite to `main.py`

Firstly, **main.py is always where you start your game program**. If you run `player.py`, **nothing will happen**.

Secondly, **You need to add "import player"** in order to tell python to include your code in player to the main program. If you run `main.py` **without the import, you won’t see your new sprite**. 

<details open markdown="block">
  <summary>
    main.py
  </summary>

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
</details>

<details open markdown="block">
  <summary>
    When you run main.py
  </summary>
  <img src="{{ site.cdn_url }}img/screenshot-sprite-creation.png" alt="img/screenshot-sprite-creation.png" width="700"/>
  You can also drag the sprite around. 
</details>


## It's Now Your Turn!
### Your task is simple: create another sprite called "enemy". 
You can use any image you like. Remember the three-step process: 
1. Put the image to `assets`
2. Open a new python file with [those lines](#2-open-a-new-file-for-the-sprite)
3. Import to `main.py`

### Tips
1. Remember to save your sprite files before running `main.py`  
2. [`pysc.create_single_costume_sprite`](#2-open-a-new-file-for-the-sprite) need to point to the image you want to use. 
3. Your project folder might look like this: 
```
├─ my_first_game/
    ├─ tutorial_pack/
    ├─ assets/
        ├─ fish_brown_outline.png
        ├─ fish_red_outline.png
    ├─ main.py
    ├─ player.py
    ├─ enemy.py
```
