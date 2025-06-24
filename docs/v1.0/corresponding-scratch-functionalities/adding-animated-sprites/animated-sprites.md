---
title: Animated Sprites
parent: Adding a Sprite
nav_order: 2
---
# Adding an Animated Sprite
## Find suitable frames for the sprites

First, put the frames in the asset folder using the following structure. You have use any name for the folder, but the images need to be numbered (will be ignored otherwise). 


**Option 1**
```
├─ my_first_game/
    ├─ assets/
        ├─ player/
            ├─ 0.png
            ├─ 1.png
            ├─ 2.png
            ...
```

**Option 2**
```
├─ my_first_game/
    ├─ assets/
        ├─ player/
            ├─ walking/
                ├─ 0.png
                ├─ 1.png
                ...
            ├─ idling/
                ├─ 0.png
                ├─ 1.png
                ...    
```

**Example Code**

```python
# create the sprite
player = pysc.create_animated_sprite('assets/player')

def animating():
    # you don't need this line here.
    # this is just to show you how to select a specific frame
    player.set_frame(0) # scratch block: switch costume to [costume0]
    
    # switch to the next frame every 0.2 second
    while True: 
        player.next_frame() # scratch block: next costume
        yield 0.2

player.when_game_start().add_handler(animating)


# if doing option 2: use `set_animation` to select the frame
# there's no equivalent scratch block
def movement():
    while True: 
        if pysc.sensing.is_key_pressed('right'): 
            player.set_animation('walking') # reference to the folder name
            player.x += 1
        else:
            player.set_animatione('idling') 
        
        yield 1/FRAMERATE

player.when_game_start().add_handler(movement)
```

## Follow through tutorial
TODO: prepare the material


## Where to find good images for my sprite
TODO: 

https://kenney.nl/assets/space-shooter-redux

https://www.gamedevmarket.net/

https://opengameart.org/content/a-platformer-in-the-forest



