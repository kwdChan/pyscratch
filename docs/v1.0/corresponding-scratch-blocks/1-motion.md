---
title: Motion
parent: Corresponding Scratch Blocks
nav_order: 1
---


# Motion
---
**move [N] steps**
- `sprite.move_indir(steps: float)`
- `sprite.move_across_dir(steps: float)`

**turn [N] degrees**
- change `sprite.direction` using `+=` or `-=`
    - 0-degree is pointing to the right
    - 90-degree is pointing downward
    - 180-degree is pointing to the left
    - -90-degree (i.e. 270-degree) is pointing to the upward


**go to [sprite/mouse/random]**
- assignment of `sprite.x`, `sprite.y`
- `pysc.helper.random_number(v_min: float, v_max: float) -> float`
    - gives you a random number
- `pysc.sensing.get_mouse_pos() -> Tuple[int, int]`
    - gives you the mouse position

**go to x: [N], y: [N]**
- assignment of `sprite.x`, `sprite.y`

**glide**
- no corresponding functions but achievable though coding

**point in direction [N]**
- assignment of `sprite.direction` 

**point towards [sprite/mouse]**
- `sprite.point_towards_sprite(sprite: ScratchSprite)`
- `sprite.point_towards_mouse()`
- `sprite.point_towards(position: Tuple[int, int])`

**change x by [N] / change y by [N]**
- change `sprite.x`, `sprite.y` using `+=` or `-=`

**set x to [N] / set y to [N]**
- assignment of `sprite.x`, `sprite.y`

**if on edge, bounce**
- no corresponding python function yet but achievable though coding

**set rotation style [rotation style]**
- `sprite.set_rotation_style_all_around()`
- `sprite.set_rotation_style_left_right()`
- `sprite.set_rotation_style_no_rotation()`

**Variable access: x position / y position / direction**
- `sprite.x`
- `sprite.y`
- `sprite.direction`


