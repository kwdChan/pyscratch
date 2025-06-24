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


### 3. Download the [Pyscratch github repo](https://github.com/kwdChan/pyscratch) into the new folder 
{: .no_toc }

Your folder should look like this: 
```
├─ my_first_game/
    ├─ pyscratch/
        ├─ ...
```

### 4. Pip install the library 
{: .no_toc }
Open the folder `my_first_game` on vscode (or `cd` into `my_first_game`) and then run `pip install -e pyscratch` in the terminal. 


### 5. You are good to go!  
{: .no_toc }



## Start the game with an empty scene
Create a new file in the folder called `main.py`

This is how the folder should look like:
```
├─ my_first_game/
    ├─ pyscratch/
    ├─ main.py
```

`main.py` is where you start the game. Put in these lines below and run the script `main.py`. 

```python
import pyscratch as pysc

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60 

# set screen size
pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# start the game with a the framerate
pysc.game.start(FRAMERATE) 
```

You should see a pygame window open. The program finishes when you close the window. 