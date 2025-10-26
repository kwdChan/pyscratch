---
title: Variables
parent: Corresponding Scratch Blocks
nav_order: 8
---

# Variables

## Adding variables
- For variables shared across the multiple sprites, put them in `pysc.game` as if it's a dictionary.
- For variables "for this sprite only", put them inside the sprite variable as if it's a dictionary.

```python
# add the variables like you'd do to a python dictionary
pysc.game['my_varible'] = "hello"
my_sprite['my_varible'] = "hello_myself"

# always access the variables inside an event to make sure it is defined when accessing.
def event():
    # access the variable like you'd do from a python dictionary
    print(pysc.game['my_varible']) # > hello
    print(my_sprite['my_varible']) # > hello_myself

my_sprite.when_game_start().add_handler(event)
```

## Display the variable for debugging purposes (experimental)
1. Add the variable to `pysc.game`
2. Create the display using <a target="_blank" href="../pdoc/pyscratch/sprite.html#create_shared_data_display_sprite"><code>pysc.create_shared_data_display_sprite</code></a> (experimental feature)


```python
font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size
pysc.game['hp'] = 10

# the variable display is created as a sprite 
health_display = create_shared_data_display_sprite('hp', font, position=(100, 100), update_period=0.5)
```