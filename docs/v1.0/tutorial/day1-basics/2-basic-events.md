---
title: Basic Events
parent: Day 1 - Basics
nav_order: 2
---

# Control the Sprite with Basic Events
{: .no_toc }

---
<details open markdown="block">
  <summary>
    In-Page Navigation
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>


## Scratch-Block Corresponding Functions
Most of the Scratch blocks has a corresponding function in PyScratch.
For example, "move 10 steps" on Scratch would be `player.move_indir(10)` in PyScratch. 

**You can find the corresponding functions of the Scratch blocks side-by-side on [this page](../corresponding-scratch-functionalities/corresponding-scratch-blocks/1-motion.md).** In a lot of the cases, you will need to replace `my_sprite` with the sprite you want to control. 


## Basic Events
For example, we want to change the size and position of the chest when it is clicked. 
<details open markdown="block">
  <summary>
    chest.py
  </summary>

```python
import pyscratch as pysc
from pyscratch import game

chest = pysc.create_single_costume_sprite("assets/chatgpt-chest-open.png")

# 1. Create a function that does the thing (any function name is fine)
def set_size_position(): 
    """
    when the chest is clicked:
    set the size and position of the chest

    Put your own description of this event here to make the code more readable
    """ 

    chest.set_scale(0.15)
    
    # the middle of the screen
    chest.x = game.screen_width/2 
    chest.y = game.screen_height/2 


# 2. Create an event object (any event name is fine)
click_event = chest.when_this_sprite_clicked() 

# 3. Attach the function to the event block
click_event.add_handler(set_size_position) 

# Or step 2 and 3 together in one line
#chest.when_this_sprite_clicked().add_handler(set_size_position) 
```
</details>

Now **save it** and run the game (by running `main.py`)!

### Creating an Event is a Mini Three-Step Process
{: .no_toc }

| |PyScratch|Scratch|
|-|-------|---------|
|**Step 1**|Create the function|Create the stack of blocks except the event block|
|**Step 2**|Create an event object (`when_this_sprite_clicked`)|Drag the event block out to the coding space|
|**Step 3**|Attach the function to the event (`add_handler`)|Attach the event block to the top of the Scratch blocks|

{: .highlight }
**The function is similar to a stack of scratch blocks without the event block at the top.** You need to attach the event block otherwise it will have no effect!


### For now, you will be able to use these two events:
{: .no_toc }
1. `when_game_start`
1. `when_this_sprite_clicked`

There are other events as well, but you need to make a small tweak to make them work. We will come to that later. 


## It's Now Your Turn!

### Task 1: Set the size and position of the chest when the game start
- Keep the same function, but use `when_game_start` instead of `when_this_sprite_clicked`

### Task 2: Make the enemy reappear in a new random location when it is clicked
- We just need to assign random numbers to the x and y of the sprite. 
- There are various way to generate a random number in Python. One easy way is to use `pysc.random_number` in PyScratch. 
<details open markdown="block">
  <summary>
    Example
  </summary>

```python
my_number = pysc.random_number(0, 100)
print(my_number) # my_number will be a random number between 0 and 100
```

</details>

### Task 3: Explore using other Scratch-block corresponding functions in the event
- For example, try making the enemy turns a little bit when you click it. 

{: .highlight }
> Remember to save the files before you run `main.py`!

### General Tips
- Checkout [this page](../corresponding-scratch-functionalities/corresponding-scratch-blocks/2-looks.md) for the corresponding blocks and functions. 
- Remember the function is just like a stack of Scratch blocks without the event at the top.

{: .text-right}
[Next Step](./3-flow-control){: .btn .btn-purple }


