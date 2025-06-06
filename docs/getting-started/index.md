---
title: Getting Started
nav_order: 1
---
# Getting Started 
---
This section shows you how to create your first minimalistic game using python. 

## Setup
### 1. Have Python installed. You only need to do it once in your computer. 

### 2. Open a new folder that will contain everything about the game

### 3. Clone the repo from [github](https://github.com/kwdChan/pyscratch) into the new folder

Your folder should look like this

```
├─ my_first_game
    ├─ pyscratch
        ├─ ...
```

### 4. Pip install the library

### 5. You are good to go! 


## Now, start the game with an empty scene
Create a file called `main.py` in the folder. This is how the folder should look like:
```
├─ my_first_game
    ├─ pyscratch
        ├─ ...
    ├─ main.py
```


Add these lines in and run the script `main.py`. 
```python
import pyscratch as pysc

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```
