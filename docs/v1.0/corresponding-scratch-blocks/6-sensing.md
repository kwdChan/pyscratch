---
title: Sensing
parent: Corresponding Scratch Blocks
nav_order: 6
---

# Sensing
---
**touching [mouse-pointer/edge/sprite]**
- `sprite_a.is_touching(sprite_b)`
- `sprite_a.is_touching_mouse()`
- edges need to be created as sprites using `pysc.create_edge_sprites()`

**touching [color] / [color1] is touching [color2]**
- impossible to implement 

**distance to [mouse-pointer/edge/sprite]**
- `sprite.distance_to(position)`
- `sprite.distance_to_sprite(another_sprite)`

**ask [question] and wait**
- not implement

**key [key] pressed**
- ``pysc.sensing.is_key_pressed(key: str)`

**mouse down**
- `pysc.sensing.get_mouse_presses() -> Tuple[int, int, int]`

**mouse x / mouse y**
- `pysc.sensing.get_mouse_pos()`

**set drag mode [draggable/not draggable]** 
- `sprite.set_draggable(True)`

**timer**
- pysc.game.current_time (milliseconds)

**variable access** 
- already mentioned above

**date/time** 
- use the python `datetime` library

**username / loudness**
- not implemented
