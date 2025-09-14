---
title: Basic Events
parent: Getting Started (New)
nav_order: 1
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
For example, we want the player to rotate and then move forward when we click it. 
<details open markdown="block">
  <summary>
    player.py
  </summary>

```python
import pyscratch as pysc

player = pysc.create_single_costume_sprite("assets/fish_brown_outline.png")

# 1. Create a function that does the thing (any function name is fine)
def rotate_move(): 
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

**Remember, the function is like a stack of scratch blocks without the event block at the top.** You need to attach the event block otherwise it will have no effect!


### For now, you will be able to use these two events:
{: .no_toc }
1. `when_game_start`
1. `when_this_sprite_clicked`

There are other events as well, but you need to make a small tweak to make them work. We will come to that later. 

## Flow Control (Loops & if/else)
I assume you already know the basics of [loops](https://www.w3schools.com/python/ref_keyword_for.asp) and [conditions(if/else)](https://www.w3schools.com/python/python_conditions.asp). 

Now I want the player to move forward when the D key is pressed.  

**This is what you would do in in Scratch:** 

<details open markdown="block">
  <summary>
    Scratch
  </summary>
PLACEHOLDER FOR IMAGE
</details>

**In PyScratch, it would be similar:** 

<details open markdown="block">
  <summary>
    player.py 
  </summary>

```python 
# Remember: The function is the stack of scratch blocks without the event block at the top
def move(): 
    while True: # the forever loop 
        if pysc.is_key_pressed("d"):  # the sensing block: 'key [w] pressed'
            player.x += 4   # the motion block: change y by [-4]

        # the control block: wait [1/60] seconds
        # because the frame rate is 60, this is basically to wait for one frame
        yield 1/60 

# Attach the function to the event
game_start = player.when_game_start() 
game_start.add_handler(move) 

# Or just in one line
#player.when_game_start().add_handler(move) 
```
</details>

### Remember to Wait (`yield`) in the Loop! 
**Python will put everything aside to run the loop as quickly as possible, unless you ask it to wait**. Without waiting, a repeat loop (`for` loop) for 1000 times will be finished almost instantly and a forever loop (`while True`) without waiting **will get the program stucked forever**.

In this library, **we use yield as as the wait block in Scratch**. For example, `yield 0.5` means wait for 0.5 second. 


## It's Now Your Turn!

### Task 1: Use the `when_this_sprite_clicked` event
- Make the enemy a bit bigger when clicked 
- If you want a challenge, make it gradually grow larger

### Task 2: Use the `when_game_start` event
- Move the player using the WASD keys
- If you want a challenge, add a key to change the speed of the player (create a variable!)

### Tips
- Checkout [this page](../corresponding-scratch-functionalities/corresponding-scratch-blocks/2-looks.md) for the corresponding blocks and functions. 
- Remember the function is just like the stack of Scratch blocks without the event at the top.
- If you find it hard, think about how you would do it if it is on Scratch. 
- Remember to wait in the loop! 

### Confusion About the Pointy Slots and the Round Slots?
<details markdown="block">
  <summary>
    Click here for a little read
  </summary>

TODO

One thing to be remember is that, conditions like (`b > a`) are just boolean variables (true/false). 

I am sure you have seen something like this before: 
```python 
if b > a:
    print('b is greater than a')
```
The above is a shorthand for the following: 
```python 
is_b_above_a = (b > a)
if is_b_above_a:
    print('b is greater than a')
```

Just like you can print a number or string, you can also print a boolean. It's just a variable after all.    
```python
print("is_b_above_a: " + str(is_b_above_a))
```

Similarly, you can do:  
```python 
the_condition_variable = (b > a) and (a > 0) or (b > 0)
# same as: if (b > a) and (a > 0) or (b > 0):
if the_condition_variable:
    print("it's true!")
else:
    print("it's false!")

print("the_condition_variable: " + str(the_condition_variable))
```

Or even:
```python 
the_condition_variable = True
# same as: if True:
if the_condition_variable:
    print("it's true!")
else:
    print("it's false!")

print("the_condition_variable: " + str(the_condition_variable))
```

</details>