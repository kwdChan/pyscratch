---
title: 5. Shared Variables 
parent: Day 1 - Basics
nav_order: 5
---

# 5. Shared Variables
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

{: .highlight }
> This tutorial requires PyScratch version 2.1.0 or above. 

## Demo 1: Create a Shared Variable  
Let's add a score for this game by creating a shared variable. 

This can be done by putting the value in this dictionary-like object `pyscratch.game`. In this example, we put these lines in the beginning of `main.py`, but you can put them anywhere in any file.  

<details open markdown="block">
  <summary>
    main.py
  </summary>

```python
import pyscratch as pysc
from pyscratch import game

game['score'] = 0
score_display = pysc.create_shared_data_display_sprite('score') 
# note that the score display is also a sprite and you can control it if you want. 
# for example, to make it draggable: 
score_display.set_draggable(True)
```
This is similar to creating a variable in Scratch under the variable tab with the display enabled. 
</details>


<details open markdown="block">
  <summary>
    Without variable display, only one line is necessary. 
  </summary>

```python
import pyscratch as pysc
from pyscratch import game

game['score'] = 0
```

</details>


{: .highlight-title}
>Note
>
>The shared variable should always be created outside the event. 


## Demo 2: Change the Variable
Let's increase the score by one when the enemy is clicked. 

<details open markdown="block">
  <summary>
    enemy.py
  </summary>

```python
# make sure this line exists on the top of the script
from pyscratch import game

@enemy.when_this_sprite_clicked()
def clicked():
    """
    change the enemy location with a fade out effect and increment the score
    """
    game['score'] += 10 # same as the Scratch block "change 'my variable' by 10"
    
    # the logic to make the enemy fade out and reappear
    ...
    
```

</details>

{: .highlight-title}
>Caveat!
>
>The access of these shared variables are guaranteed only inside the events. 
>
>If you try to access (or change) a shared variable from outside the events, you may or may not encounter an error, depending on many arbitrary factors. 


## It's Now Your Turn!
### Task 1: Increase the score by 10 when the friend fish arrives at the chest 
- Increase the score before the friend fish reappears after arriving the chest (the centre of the window)

### Task 2: Continuously reduce the score when the enemy is at the chest  
- Create a new event, inside a forever loop, check if the enemy is within a certain distance to the centre of the window
- If so, reduce the score by 1.
- Yield for 0.1 second (so the score decreases by 10 for each second the enemy is in the centre)

### Task 3: Make the enemy moves faster when the score is higher
- For example, make the speed a constant plus a percentage of the score
  - `speed = 5 + game['score']*0.1`


<details open markdown="block">
  <summary>
    The game might look like this
  </summary>

  <video autoplay loop muted playsinline style="max-width: 100%"  width="500">
    <source src="{{ site.cdn_url }}tut-day1/4-1.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video>    

</details>



{: .text-right}
[Next Step](./6-backdrop){: .btn .btn-purple }

