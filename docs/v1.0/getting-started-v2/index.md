---
title: Getting Started (New)
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
### 1. Install Python and <a href="https://code.visualstudio.com/download" target="_blank">VSCode</a>
{: .no_toc }


### 2. Open a new folder for your game on VSCode 
{: .no_toc }
Name the new folder, let say, `my_first_game`


### 3. Install PyScratch
{: .no_toc }
On the terminal, run this to install PyScratch globally:
```bash
pip install pyscratch-pysc
```

Alternatively, if you need to install it in a <a target="_blank" href="https://python.land/virtual-environments/virtualenv">virtual environment</a>, 
`cd` into your your project folder (`my_first_game` in this case), and then run this:  

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyscratch-pysc
```
Note that this library is `pyscratch-pysc` on pip instead of `pyscratch`. `pyscratch` on pip is another Python library that has no association with this library.   

### 4. You are good to go! 
{: .no_toc }





## Start the game with an empty scene
Create a new file in the folder called `main.py`. 
**This script is where you start the game.**

Put in these lines below and run the script `main.py`. 


```python
import pyscratch as pysc

WIN_WIDTH = 500 # change me
WIN_HEIGHT = 500 # change me
FRAMERATE = 60 

# set screen size
pysc.game.update_screen_mode((WIN_WIDTH, WIN_HEIGHT)) 

# start the game with a the framerate
pysc.game.start(FRAMERATE) 
```

You should see a pygame window open. The program finishes when you close the window. 
You can also exit the program by pressing the escape key (Esc). 

You can adjust the window size by changing the value of `WIN_WIDTH` and `WIN_HEIGHT`. 



## This is how the folder should look like
{: .no_toc }

```
├─ my_first_game/
    ├─ main.py
```

