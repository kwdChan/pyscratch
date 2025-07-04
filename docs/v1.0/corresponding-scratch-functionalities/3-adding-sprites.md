---
title: Adding a Sprite
parent: Corresponding Scratch Functionalities
nav_order: 3
---

# Adding a Sprite

## 1. Create the Art for the Sprite
Adding a sprite to the game is very easy - just one line of code and it's done. The hard part is to create the art to give life to your sprites. Follow this [guide](../asset-preparation-guide/) to learn how to do it. 


## 2. Adding the Sprite to the Game
For a step-by-step guide, follow [this tutorial](../getting-started/1-create-the-first-sprite.html)

**First, create a new file for the sprite.** 
<details open markdown="block">
  <summary>
    player.py
  </summary>

```python
import pyscratch as pysc

the_player = pysc.create_single_costume_sprite("assets/player-fish.png")
```
</details>

**Second, import it in main.py**

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
import player # reference to the filename (player.py, not the variable name `the_player`)

# start the game
pysc.game.update_screen_mode((1280, 720))
pysc.game.start(60)
```
</details>


## All the functions that create a sprite

**Basic shapes**
- <a target="_blank" href="../pdoc/pyscratch/sprite.html#create_rect_sprite"><code>pysc.create_rect_sprite</code></a>
- <a target="_blank" href="../pdoc/pyscratch/sprite.html#create_circle_sprite"><code>pysc.create_circle_sprite</code></a>

**Single costume sprite** 
- <a target="_blank" href="../pdoc/pyscratch/sprite.html#create_single_costume_sprite"><code>pysc.create_single_costume_sprite</code></a>


**Animated sprite** (multiple costumes and animations)
- <a target="_blank" href="../pdoc/pyscratch/sprite.html#create_animated_sprite"><code>pysc.create_animated_sprite</code></a> 


**For a more custom sprite (advance)**
- <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite"><code>pysc.Sprite</code></a>


Continue to learn more about creating a sprite.
 
{: .d-flex .flex-justify-end }
[Next](./1-single-costume-sprite.md){: .btn .btn-purple }
