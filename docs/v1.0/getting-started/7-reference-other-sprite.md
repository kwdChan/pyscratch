---
title: Referencing Other Sprites
parent: Getting Started
nav_order: 7
---
# Referencing Other Sprites
---

## Collision Detection
In Scratch, if you want to detect the collision between two sprites, you use the sensing block "touching" and then you select the sprite of which you want the collision to be detected. In Python, you pass in the sprite variable to the function. 

Let say you want something to happen when the player touches the enemy fishes, you first need to make the player sprite accessible by adding it to `pysc.game` like you did earlier. 

```python
# you can add this line anywhere in player.py after the player sprite is created (ideally immediately after) 
pysc.game['player'] = player
```


Now, you can detect the collision by adding this event to `enemy.py`

```python 

# clone touch the player 
def clone_touch_the_player(clone_sprite):
    player = pysc.game['player']
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()
        yield 1/60
    
enemy.when_started_as_clone().add_handler(clone_touch_the_player)
```

Note that in this library, the parent and clones are treated as separate sprites. So `player.is_touching(enemy)` will only detect the touching between the player and the parent enemy, not clone enemies. Therefore, the touching of the clone should be detected by the clone instead of the player. 

<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/collision-detection.png" alt="img/collision-detection" width="200"/>
</details>



## Put everything together
Update the game, so 
1. There are 3 HP of the player 
2. Collisions with the enemies reduce 1HP 
3. When HP reach zero, the player is removed
4. The enemies follow the player when the player is within a certain distance
5. There is a display of the HP

See `my_first_game/pyscratch/example/getting-started/step 7 - Referencing other sprites` for the code. 

See [getting-started](index.md#optional-run-each-step-of-this-tutorial-in-your-own-computer) to run this step in your own computer.

<details open markdown="block">
  <summary>
    What you would see in the game
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%;">
    <source src="vid/referencing.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>