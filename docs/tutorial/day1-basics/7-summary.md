---
title: Summary
parent: Day 1 - Basics
nav_order: 7
---
# Summary

## Things You Have Learn Today
1. How to create a single costume sprite
1. Three types of events
    - `when_game_start` 
	- `when_this_sprite_clicked`
	- `when_backdrop_switched` 
1. Flow Control
	- Using loops with `yield`
	- Using `if/else` with Boolean variables (hexagon blocks)
1. Shared Variables (and the display)
1. Backdrop & Sound
1. Most of the [functions that correspond to a Scratch block](../../corresponding-scratch-blocks/) *except* 
	- Those that reference to other sprites (day 2)
	- The other events that hasn't been mentioned yet (day 3)


## Yet to Learn
- Sprites with multiple costume
- Blocks that references to another sprite (such as `is_touching`)
- Other events


## Exercises: Improve the Game
### 1. Add a targeting crosshair to the cursor 
{: .d-inline-block}

Easy - LV1 
{: .label .label-green}

- Put the crosshair image to the asset folder
- Create the sprite with the image and import it to `main.py`
- Add a `when_game_start` event, with a forever loop:
	- Move the sprite to the cursor
	- Yield for one frame (or 1/60 second)
- Optional: Bring the sprite to the front layer in the `when_game_start` event before the loop


<details open markdown="block">
  <summary>
    Optional: Add these two lines on the top of `main.py` to hide the mouse
  </summary>

```python
import pygame
pygame.mouse.set_visible(False)
```

</details>

<details open markdown="block">
  <summary>
    Outcome
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/7-1.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>

### 2. Add visual and audio effects for clicking the friend 
{: .d-inline-block}

Easy - LV1 
{: .label .label-green}

- Put a audio file to the asset folder
- Add a `when_this_sprite_clicked` event for the friend
	- Play the sound 
	- In a repeat (`for`) loop, flash the friend by showing and hiding it.  


<details open markdown="block">
  <summary>
    Outcome
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/7-2.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>

### 3. Add words at the end of the game
{: .d-inline-block}

Intermediate - LV2
{: .label .label-yellow}

- Create an image with the word "You Lose" or "Game Over" using Piskel
- Create a sprite with the image and hide it on game start
- Show the sprite when the game switch to the backdrop `"lose"`

<details open markdown="block">
  <summary>
    Outcome
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/7-3.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>

### 4. Spin the enemy when clicked
{: .d-inline-block}

Hard - LV3
{: .label .label-red}

To spin the enemy, you need to increment the enemy's `direction` inside the repeat loop of the `when_this_sprite_clicked` event. 

However, we already have a forever loop that continuously changes the enemy's `direction` to control its movements. This will intervene the spinning of the enemy. 

Therefore, you need to create a shared variable to tell your forever loop not to change the enemy's `direction` when you are spinning the enemy. 

<details markdown="block">
  <summary>
    Detailed Instruction
  </summary>
  
- Create a shared variable `"spinning"`, default to `False`
- In the `when_this_sprite_clicked` event,
	- Set `"spinning"` to `True`
	- Turn the enemy by incrementing the `direction` inside the repeat loop (`for` loop)
	- Set `"spinning"` back to `False`
- In the event where you move the enemy
	- If `"spinning"` is `True`, do not run `point_towards_mouse` and the related logics. 
 

</details>

<details open markdown="block">
  <summary>
    Outcome
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/7-4.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>


### 5. Add a perk that you can click to slow down the enemy
{: .d-inline-block}

Hard - LV3
{: .label .label-red}

- Create a sprite when the any desired image
- Create a shared variable called `"speed_multiplier"`, default to 1.0
- In a `when_this_sprite_clicked` event
	- Hide the sprite
	- Move the sprite to a random location 
	- Multiply `"speed_multiplier"` by 0.9
- In a `when_game_start` event, with a forever loop
	- Yield for a random amount of time
	- Show the sprite 
- In the event where you move the enemy 
	- Multiple the enemy's speed by `"speed_multiplier"`


<details open markdown="block">
  <summary>
    Outcome
  </summary>
  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/7-5.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>
