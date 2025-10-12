---
title: Loops & Conditions (if/else)
parent: Day 1 - Basics
nav_order: 3
---

# Loops & Conditions (if/else)
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

I assume you already know the basics of [loops](https://www.w3schools.com/python/ref_keyword_for.asp) and [conditions (if/else)](https://www.w3schools.com/python/python_conditions.asp). 

## Using Loops and Conditions

### Demo 1: Fade out effect when the enemy is clicked
**We want the enemy to shrink and fade out when it is clicked before it reappears somewhere else**.  

This is what you would do in in Scratch:

<details open markdown="block">
  <summary>
    Scratch
  </summary>
PLACEHOLDER FOR IMAGE
</details>

In PyScratch, it would be similar:
<details open markdown="block">
  <summary>
    enemy.py 
  </summary>

```python 

def clicked():
    """
    when the enemy is clicked: 
    change the enemy location with a fade out effect
    """
    # make the enemy smaller and paler 
    for i in range(10): # this is a repeat loop (10 repeats)
        yield 0.05 # wait for 0.05 second
        enemy.set_transparency(1-i/10) # make the enemy paler each step. if you find this confusing, do print(1-i/10) 
        enemy.scale_by(0.9) # make the enemy 10% smaller each step

    # change the location of the enemy
    enemy.x = pysc.random_number(0, game.screen_width)
    enemy.y = pysc.random_number(0, game.screen_height)

    # put the size and transparency back to normal
    enemy.set_transparency(1)
    enemy.set_scale(1)
    
enemy.when_this_sprite_clicked().add_handler(clicked)

```
</details>

### Wait (`yield`) in the Loop

{: .highlight-title }
> It is essential to wait (yield) in the loop!
> 
> **Python will put everything aside to run the loop as quickly as possible, unless you ask it to wait**. Without waiting, a repeat loop (`for` loop) for 1000 times will be finished almost instantly and a forever loop (`while True`) without waiting will get the program stucked forever.
> 
> In this library, **we use yield as the wait block in Scratch**. For example, `yield 0.5` means wait for 0.5 second. 


### Demo 2: Enemy Movement using a Forever Loop
**We want the enemy to move to the centre of the window but avoid the mouse when it's close.**.  

<details open markdown="block">
  <summary>
    enemy.py 
  </summary>

```python 
# Remember: The function is the stack of scratch blocks without the event block at the top
def movement():
    """
    when_game_start: 
    the movement of the enemy

    Put your own description of this event here to make the code more readable
    """

    speed = 5
    centre = (game.screen_width/2, game.screen_height/2)

    while True:
        # wait for one frame 
        yield 1/60 # or 1/game.framerate

        # get the enemy's distance to the cursor location
        mouse_x, mouse_y = pysc.get_mouse_pos()
        distance_to_mouse = enemy.distance_to((mouse_x, mouse_y))

        # enemy avoids the mouse when it is close to the mouse
        if distance_to_mouse < 200: 
            enemy.point_towards_mouse()
            enemy.direction += 180
            enemy.move_indir(speed)
        
        # otherwise, go to the centre of the screen 
        else:
            enemy.point_towards(centre)
            enemy.move_indir(speed)


enemy.when_game_start().add_handler(movement)

```
</details>


### Hexagon Slots and the If-Statement
In Scratch, the if-block would have a hexagon slot that only takes in the hexagon blocks. 

<details open markdown="block">
  <summary>
    PLACEHOLDER
  </summary>

  PLACEHOLDER
</details>

These hexagon blocks are always some sorts of a condition, that can only be one of the two states: True or False. In Python, this is known as a boolean variable. 

The `if` keyword always expect a boolean variable to follow.


<details open markdown="block">
  <summary>
    Example
  </summary>
These four if-statements below are all valid and almost equivalent. 

```python
mouse_x, mouse_y = pysc.get_mouse_pos()
distance_to_mouse = enemy.distance_to((mouse_x, mouse_y))
is_close_to_mouse = distance_to_mouse < 200

# all these four ways are valid and almost equivalent
if is_close_to_mouse:
    pass
if distance_to_mouse < 200: 
    pass
if enemy.distance_to((mouse_x, mouse_y)) < 200: 
    pass
if enemy.distance_to(pysc.get_mouse_pos()) < 200: 
    pass
```
</details>




## It's Now Your Turn!

### Task 1: Experiment with `yield`
- Try removing the `yield` line in the first demo event (in the for loop)
- Try removing the `yield` line in the second demo event (in the while loop) - Expect the program to freeze!
- Try putting a longer or shorter wait time in the demo events

{: .highlight }
> Remember to save the sprite files before running `main.py`!

### Task 2: Add a new sprite, named "friend"
- Use an image of a fish for this sprite. 

{: .highlight }
> Remember to import the new sprite to `main.py`!

### Task 3: Add the movement of the friend fish 
- The friend fish should have the same movement logic as the enemy: 
  - It moves to the centre of the screen.
  - It avoids the cursor when it is getting close.   

### Task 4: The friend fish disappears and reappears somewhere random when it is near the centre of the window
- When the distance of the friend fish to the centre is smaller than a certain threshold, change its location randomly. 
- You can create a new `when_game_start` event with a forever loop to check this condition. 

### Tips
- Remember the function is just like the stack of Scratch blocks without the event at the top.
- If you find it hard, think about how you would do it if it is on Scratch. 
- Remember to wait in the loop! 
- Remember to save the files before you run. 



{: .text-right}
[Next Step](./4-variables){: .btn .btn-purple }


