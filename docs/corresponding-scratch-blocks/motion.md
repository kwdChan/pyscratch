---
title: Motion
parent: Corresponding Scratch Blocks
nav_order: 1
---


# Motion
---
**move [N] steps**
- `sprite.move_indir`
- `sprite.move_across_dir`
- `sprite.move_xy`

**turn [N] degrees**
- `sprite.add_rotation`

**go to [sprite/mouse/random] / go to x: [N] y: [N]**
- access and assignment of `sprite.x`, `sprite.y`
- `pysc.helper.random_number`
- `pysc.sensing.get_mouse_pos`

**glide**
- no correspondence but achievable though coding

**point in direction**
- `sprite.set_rotation`

**point towards [sprite/mouse]
- `sprite.point_towards(position: Tuple[int, int])`
- `sprite.point_towards_sprite(sprite: ScratchSprite)`
- `sprite.point_towards_mouse()`

**change x by [N] / change y by [N]**
- change `sprite.x`, `sprite.y` using `+=`

**set x to [N] / set y to [N]**
- assignment of `sprite.x`, `sprite.y`

**if on edge, bounce**
- no corresponding python function but achievable though coding

**set rotation style [rotation style]**
- no corresponding python function but very easy to workaround 

variable access: **x position / y position / direction**
- `sprite.x`
- `sprite.y`
- `sprite.direction`


