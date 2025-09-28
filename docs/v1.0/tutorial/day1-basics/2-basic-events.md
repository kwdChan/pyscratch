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
For example, we want the player to rotate and then move forward *1.5 second after* when we click it. 
<details open markdown="block">
  <summary>
    player.py
  </summary>

```python
import pyscratch as pysc

player = pysc.create_single_costume_sprite("assets/fish_brown_outline.png")

# 1. Create a function that does the thing (any function name is fine)
def rotate_move(): 
    yield 1.5 # wait for 1.5 seconds
    player.direction += 90
    player.move_indir(50)

# 2. Create an event object (any event name is fine)
click_event = player.when_this_sprite_clicked() 

# 3. Attach the function to the event block
click_event.add_handler(rotate_move) 

# Or step 2 and 3 together in one line
#player.when_this_sprite_clicked().add_handler(rotate_move) 
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
**The function is like a stack of scratch blocks without the event block at the top.** You need to attach the event block otherwise it will have no effect!


### For now, you will be able to use these two events:
{: .no_toc }
1. `when_game_start`
1. `when_this_sprite_clicked`

There are other events as well, but you need to make a small tweak to make them work. We will come to that later. 


## It's Now Your Turn!

### Task 1: Use the `when_this_sprite_clicked` event
- Without using loops, make the player *gradually* grow bigger over two seconds after clicked

### Task 2: Use the `when_game_start` event
- Put the enemy to the centre of the window 
- Hide the enemy when the game start
- Show the enemy 5 seconds after the game start

{: .highlight }
> Remember to save the files before you run `main.py`!

### Tips
- Checkout [this page](../corresponding-scratch-functionalities/corresponding-scratch-blocks/2-looks.md) for the corresponding blocks and functions. 
- Remember the function is just like the stack of Scratch blocks without the event at the top.
- If you find it hard, think about how you would do it if it is on Scratch. 
- Remember to wait in the loop! 

{: .text-right}
[Next Step](./3-flow-control){: .btn .btn-purple }


