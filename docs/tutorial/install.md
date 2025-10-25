---
title: Installation
nav_order: 0
parent: Tutorial
---
# Installation
{: .no_toc }

---

This section shows you how to install PyScratch on your computer.

<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Installation 
### 1. Install Python and <a href="https://code.visualstudio.com/download" target="_blank">VSCode</a>
{: .no_toc }


### 2. Open a new folder for your game on VSCode 
{: .no_toc }
Name the new folder, let say, `my_first_game`


### 3. Install PyScratch
{: .no_toc }
On the terminal, run this to install PyScratch:
```bash
pip install pyscratch-pysc
```

{: .highlight }
> Note that this library is `pyscratch-pysc` on pip. `pyscratch` on pip is another Python library that has no association with this library.   

<details markdown="block">
  <summary>
    If you are installing on Windows
    </summary>

Continue with this guide and try to start the game with an empty scene. 

If you get a`ModuleNotFoundError: No module named 'pyscratch'` when you run the empty scene, your vscode might be using another Python installation that is different to the one that the default `pip` uses. 

In this case, you should use the following line but substitute `/path/to/python.exe` with the path of the Python installation that your vscode uses. 

```bash
/path/to/python.exe -m pip install pyscratch-pysc
```

You can find the path from the terminal before the path of your script when you click the Run button on vscode. 
```
username@pc-name:/working/dir$ /path/to/python.exe /path/to/script/main.py
Traceback (most recent call last):
...
```

</details>

### 4. You are good to go! 
{: .no_toc }


## Start the game with an empty scene

Create a new file in the project folder called `main.py`. 
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

