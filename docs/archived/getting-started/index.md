---
title: Getting Started (Outdated)
parent: Archived Pages
nav_order: 1
---
# Getting Started (Outdated)
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


## Optional: Run each step of this tutorial in your own computer
**1. Set the working directory**

Open the terminal in vscode, set the folder `my_first_game/pyscratch/example/getting-started` as your working directory using the `cd` command. 
The `cd` command set a folder inside the current working directory to be the new working directory. 

For example, assuming that you have the folder `my_first_game` opened in vscode, the default working directory of your terminal in vscode would be `my_first_game`. 
So just run `cd pyscratch/example/getting-started` in the terminal. 



**2. Open `main.py` of step you want to run, and click the run button near the top-left corner.** 


<details open markdown="block">
  <summary>
    Video Guide
  </summary>
  <video controls autoplay loop muted playsinline style="max-width: 100%;">
    <source src="{{ site.cdn_url }}vid/running-examples_down.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    
</details>
