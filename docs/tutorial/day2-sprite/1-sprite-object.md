---
title: Controlling a Specific Sprite
parent: Day 2 - Sprite
nav_order: 1
---
# Controlling a Specific Sprite
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


## Controlling Multiple Sprites in an Event
Unlike Scratch, you are not limited to have only one sprite in a file. 

In PyScratch, you can do the following: 

<details open markdown="block">
  <summary>
    player.py 
  </summary>

```python 
import pyscratch as pysc

player1 = pysc.create_single_costume_sprite("assets/fish_brown_outline.png")
player2 = pysc.create_single_costume_sprite("assets/fish_orange_outline.png")

def move(): 
    while True:
        if pysc.is_key_pressed("d"):  
            player1.x += 4   

        if pysc.is_key_pressed("left"):  
            player2.x += 4   

        yield 1/60  # must have an yield in a loop! 

# for the purpose of this tutorial, 
# `player1.when_game_start()` and `player2.when_game_start()` are almost the same. 
game_start = player2.when_game_start()  
game_start.add_handler(move) 

```


</details>

Notice that you this is one event controlling two sprites. 


## Creating a Sprite in an Event 
You can even create sprites within an event: 

<details open markdown="block">
  <summary>
    enemy.py 
  </summary>
  
```python 
import pyscratch as pysc

spawn_button = pysc.create_single_costume_sprite("assets/button.png")

def spwan_enemy(): 
    enemy_red = pysc.create_single_costume_sprite("assets/fish_red_outline.png")
    enemy_blue = pysc.create_single_costume_sprite("assets/fish_blue_outline.png")

    enemy_blue.x = game.screen_width 
    
    while True:
        enemy_red.x += 4
        enemy_blue.x -= 4

        yield 1/60  # must have an yield in a loop! 
    
spawn_button.when_this_sprite_clicked().add_handler(move) 

```
</details>


In this simple example, the sprites `enemy_red` and `enemy_blue` are created and controlled directly by the event. But for more complex behaviours, you will need to create event within the event. The procedure to create the events is exactly the same (the 3-step process) but just inside the function. [TODO: Link to an example]



## It's Now Your Turn!

### Task: Make both players move
Make `player1` move by the WASD keys and `player2` by the left, right, up and down keys.



### Bonus Challenge: Collision detection
Can you find out how to detect the collision between `player1` and `player2`?  
If so, make both players disappear upon the collision.
