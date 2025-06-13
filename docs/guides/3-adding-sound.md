---
title: Adding Sound
parent: Guides
nav_order: 3
---
# Adding Sound
## 1. Put the audio file into the asset folder
```
├─ my_first_game/
    ...
    ├─ assets/
        ├─ Metal Clang.wav
```

## 2. Load the track in main.py
```python
pysc.game.load_sound('pong', 'assets/Metal Clang.wav')
```

## 3. When you need to play the sound, anywhere in the game
```python
# play the sound at 70% volume
pysc.game.play_sound('pong', volume=0.7)
```


## Where to find good sound effects
https://freesound.org/

https://soundbible.com/1781-Metal-Clang.html

https://www.freesoundeffects.com/
