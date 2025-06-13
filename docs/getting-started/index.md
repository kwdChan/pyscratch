---
title: Getting Started
nav_order: 1
---
# Getting Started 
{: .no_toc }

---
This section shows you how to create your first example game using python. 

<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Setup 
### 1. Have Python installed. You only need to do it once in your computer. 
{: .no_toc }


### 2. Open a new folder that will contain everything about the game 
{: .no_toc }
Name the new folder, let say, `my_first_game`


### 3. Clone the [Pyscratch github repo](https://github.com/kwdChan/pyscratch) into the new folder 
{: .no_toc }


Your folder should look like this

```
├─ my_first_game/
    ├─ pyscratch/
        ├─ ...
```

### 4. Pip install the library 
{: .no_toc }
Open the folder `my_first_game` using vscode, and then run 
`pip install -e pyscratch`


### 5. You are good to go!  
{: .no_toc }



## Start the game with an empty scene
Create two files in the folder, one called `main.py`, another one called `settings.py` 

This is how the folder should look like:
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ main.py
    ├─ settings.py
```

`settings.py` is where you put some constant variables for the entire game. For now, you only need these three lines in this file.

```python
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60 # 60 frames per second
```
`main.py` is where you start the game. Put in these lines below and run the script `main.py`. 

```python
import pyscratch as pysc
from settings import * # import all the variables from settings.py

# set screen size
pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# start the game with a the framerate
pysc.game.start(FRAMERATE) 
```

You should see a pygame window open. The program finishes when you close the window. 