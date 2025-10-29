---
title: 2. Event Basics
parent: Day 1 - Basics
nav_order: 2
---

# 2. Event Basics

When you first learn Python, the script you run might look like this:
<details open markdown="block">
  <summary>
    Code
  </summary>

```python
message = "I am a chest! "
n_repeat = 4
print(f"print message: '{message}' {n_repeat} times")

repeated_message = message * n_repeat
print(repeated_message)
```
</details>

When you run script, the script runs from the first line to the last line **only once**. 

<details open markdown="block">
  <summary>
    Output
  </summary>
```
print message: 'I am a chest! ' 4 times
I am a chest! I am a chest! I am a chest! I am a chest! 
```
</details>


## Let the Event Run the Code

But we don't want the code to run just once. We want the code to run whenever *something* happens in the game! 

This is where the ***Event*** comes in.

### Step 1: Put the code in a function
```python
def my_click_event():
    message = "I am a chest! "
    n_repeat = 4
    repeated_message = message * n_repeat
    print(repeated_message)
```

Now you can run the code whenever you want, for as many times as possible. 

```python
my_click_event()
print("Call it again!")
my_click_event()
print("Call it again!")
my_click_event()
print("That's enough.")
```


<details open markdown="block">
  <summary>
    Output
  </summary>
```
I am a chest! I am a chest! I am a chest! I am a chest! 
Call it again!
I am a chest! I am a chest! I am a chest! I am a chest!
Call it again!
I am a chest! I am a chest! I am a chest! I am a chest! 
That's enough.
```
</details>


### Step 2: Let the game run your functions
You forgo the ablity to call the function by yourself, and let PyScratch run it for you. 

We used the `when_this_sprite_clicked` event in this case. 

We just add this line on top of the function `@<sprite>.when_this_sprite_clicked` and replace `<sprite>` with your sprite. 

{: .highlight }
> Requires PyScratch version 2.1.0 or above. 

```python
@chest.when_this_sprite_clicked()
def my_click_event():
    message = "I am a chest! "
    n_repeat = 4
    repeated_message = message * n_repeat
    print(repeated_message)
```

Now put in `chest.py`, save it, and run `main.py`. 

<details open markdown="block">
  <summary>
    The game running your function
  </summary>
  <video autoplay loop muted controls playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/event-1.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video> </details>


### Multiple events
When you have multiple events, just out the events one after another. 
The order of the events does not matter. 

<details open markdown="block">
  <summary>
    chest.py
  </summary>

```python
import pyscratch as pysc
from pyscratch import game

chest = pysc.create_single_costume_sprite("assets/chest-open.png")

@chest.when_this_sprite_clicked()
def click_event1():
    pass

@chest.when_this_sprite_clicked()
def cick_event2():
    pass

@chest.when_game_start()
def game_start_event1():
    pass
```
</details>


## Other Events
For now, we focus only on these two events
- `@<sprite>.when_this_sprite_clicked`
- `@<sprite>.when_game_start`

The other events take in parameters and will thus be introduced in the future. 

{: .text-right}
[Next Step](./3-coordinates){: .btn .btn-purple }

