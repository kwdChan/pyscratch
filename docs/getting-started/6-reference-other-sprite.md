---
title: Referencing Other Sprites
parent: Getting Started
nav_order: 6
---
# Referencing Other Sprites
---

In Scratch, if you want to detect the collision between two sprites, you use the sensing block "touching" and then you select the sprite of which you want the collision to be detected. In Python, you pass in the sprite variable to the function. 

Let say you want something to happen when the player touches the enemy fishes, you first need to make the player sprite accessible by adding it to the `pysc.game.shared_data` like you did earlier. 

```python
# you can add this line anywhere in player.py after the player sprite is created
pysc.game.shared_data['player'] = player
```


Now, you can detect the collision by adding this event to `enemy.py`

```python 

# clone touch the player 
def clone_touch_the_player(clone_sprite):
    player = pysc.game.shared_data['player']
    while True:
        if clone_sprite.is_touching(player):
            clone_sprite.remove()
        yield 1/FRAMERATE
    
enemy.when_started_as_clone().add_handler(clone_touch_the_player)
```

Note that in this library, the parent and clones are treated as separate sprites. So `player.is_touching(enemy)` will only detect the touching between the player and the parent enemy, not clone enemies. Therefore, the touching of the clone should detected by the clone instead of the player. 

<details open markdown="block">
  <summary>
    Analogous Scratch Code
  </summary>
  <img src="img/collision-detection.png" alt="img/collision-detection" width="200"/>
</details>



