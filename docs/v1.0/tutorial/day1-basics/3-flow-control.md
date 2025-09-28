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

## Using the Forever Loop and the If Condition

**Now we want the player to move forward when the D key is pressed**.  

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
        yield 1/60  # must have an yield in a loop! 

# Attach the function to the event
game_start = player.when_game_start() 
game_start.add_handler(move) 

# Or just in one line
#player.when_game_start().add_handler(move) 
```
</details>

### 1. Wait (`yield`) in the Loop

{: .highlight-title }
> It is essential to wait (yield) in the loop!
> 
> **Python will put everything aside to run the loop as quickly as possible, unless you ask it to wait**. Without waiting, a repeat loop (`for` loop) for 1000 times will be finished almost instantly and a forever loop (`while True`) without waiting will get the program stucked forever.
> 
> In this library, **we use yield as the wait block in Scratch**. For example, `yield 0.5` means wait for 0.5 second. 

### 2. Hexagon Slots
In Scratch, the IF block would have a hexagon slot that only takes in the hexagon blocks. 

<details open markdown="block">
  <summary>
    PLACEHOLDER
  </summary>

  PLACEHOLDER
</details>

These hexagon blocks are always some sorts of a condition, that can only be one of the two states: True or False. In Python, this is known as a boolean variable. 

The `if` keyword always expect a boolean variable to follow. 

## It's Now Your Turn!
### Task 1: Use the repeat loop (`for` loop)
1. Use the `for` loop to make the player *gradually* grow bigger over two seconds after clicked
2. Find out what would happen if you do not wait (`yield`) in the loop 

### Task 2: Move the player using the WASD keys
- Use only the `when_game_start` event
- Move the player using the WASD keys

{: .highlight }
> Remember to save the files before you run `main.py`!

### Tips
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


{: .text-right}
[Next Step](./4-variables){: .btn .btn-purple }


