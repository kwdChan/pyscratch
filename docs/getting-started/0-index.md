---
title: Getting Started
nav_order: 1
---
# Getting Started 
{: .no_toc }

---
This section shows you how to create your first minimalistic flappy bird game using python. 

<details open markdown="block">
  <summary>
<<<<<<< HEAD:docs/getting-started/0-index.md
    In-Page Navigation
=======
    In-page navigation 
>>>>>>> 35903ad76c90555c51acedbe973fb718eb7e012e:docs/getting-started/index.md
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


### 3. Clone the repo from [github](https://github.com/kwdChan/pyscratch) into the new folder 
{: .no_toc }


Your folder should look like this

```
├─ my_first_game
    ├─ pyscratch
        ├─ ...
```

### 4. Pip install the library 
{: .no_toc }


### 5. You are good to go!  
{: .no_toc }



## Start the game with an empty scene
Create a file called `main.py` in the folder. This is how the folder should look like:
```
├─ my_first_game
    ├─ pyscratch
        ├─ ...
    ├─ main.py
```


Add these lines in and run the script `main.py`. You should see a pygame window open. The program finishes when you close the window. 

```python
import pyscratch as pysc

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAMERATE = 60

pysc.game.update_screen_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pysc.game.start(FRAMERATE)
```
