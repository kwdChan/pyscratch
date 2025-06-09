---
title: Sensing
parent: Corresponding Scratch Blocks
nav_order: 6
---

# Sensing
---
**touching [mouse-pointer/edge/sprite]**
- `pysc.sensing.is_touching(sprite_a, sprite_b)`
- `pysc.sensing.is_touching_mouse(sprite)`
- `sprite.is_touching(sprite_b)`
- edges are created as sprites

**touching color / color is touching color**
- impossible to implement and unimportant

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

**set drag mode** 
- `sprite.set_draggable(True)`

**timer**
- pysc.game.current_time (milliseconds)

**variable access** 
- already mentioned above

**date/time** 
- use the python `datetime` library

**username / loudness**
- not implemented
