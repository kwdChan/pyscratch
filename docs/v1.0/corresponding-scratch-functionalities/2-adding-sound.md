---
title: Adding Sound
parent: Corresponding Scratch Functionalities
nav_order: 2
---
# Adding Sound

## 1. Find a suitable sound effect or audio track
Here are some of the sound effect libraries:
- <a target="_blank" href="https://freesound.org/">freesound</a>
- <a target="_blank" href="https://soundbible.com/1781-Metal-Clang.html">soundbible</a>
- <a target="_blank" href="https://www.freesoundeffects.com/">freesoundeffects</a>


## 2. Put the audio file into the asset folder
```
├─ my_first_game/
    ├─ assets/
        ├─ Metal Clang.wav
```

## 3. Load the track in main.py
```python
pysc.game.load_sound('pong', 'assets/Metal Clang.wav')
```

## 4. When you need to play the sound, anywhere in the game
```python
game.play_sound('pong')

# or 

game.play_sound('pong', 0.7) # play the sound at 70% volume
```

## Example 

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
import sprite1, sprite2

pysc.game.load_sound('pong', 'assets/Metal Clang.wav')

# start the game
pysc.game.update_screen_mode((1280, 720))
pysc.game.start(60)
```
</details>

<details open markdown="block">
  <summary>
    sprite1.py
  </summary>

```python
import pyscratch as pysc

sprite1 = pysc.create_animated_sprite("assets/sprite1")

def check_collision():
    while True: 
        if sprite1.is_touching(pysc.game['sprite2']):
            game.play_sound('pong')
        yield 1/60

sprite1.when_game_start().add_handler(check_collision)
    
```
</details>


