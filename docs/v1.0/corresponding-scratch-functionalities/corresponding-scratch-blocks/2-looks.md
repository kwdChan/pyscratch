---
title: Looks
parent: Corresponding Scratch Blocks
nav_order: 2
---
# Looks
---
**say/think [text] for N seconds**
- not implemented yet but a work around is provided using extended features (not scratch corresponding)
- will likely be implemented in the future 

**switch costume to [costume]  / next costume**
- `sprite.set_frame(index: int)`
- `sprite.next_frame()`
- extended feature: `sprite.set_animation(mode: str)`

**switch backdrop to [backdrop] / next backdrop**
- `pysc.game.switch_backdrop(index: int)`
- `pysc.game.next_backdrop()`

**change size by [N]** / **set size to [N] %**
- `sprite.scale_by(factor: float)`
- `sprite.set_scale(factor: float)`

**change [effect] effect by [N]** / **set [effect] effect by [N]**
- `sprite.set_transparency`
- `sprite.set_brightness`
- other effects are not implemented (deemed not important)
- no corresponding python method for "change by". use set instead. 

**clear graphic effects**
- no corresponding python function
- just set the effects to 1

**show** / **hide**
- `sprite.show()`
- `sprite.hide()`

**go to [front/back] layer**
- `pysc.game.move_to_back(sprite)`
- `pysc.game.bring_to_front(sprite)`

**go \[forward/backward\] \[N\] layers**
- `pysc.game.change_layer_by(sprite, by: int)`
- `pysc.game.change_layer(sprite, layer: int)`

variable access: **costume number, backdrop number, size**
- `sprite.animation_name`, `sprite.frame_idx`
- `sprite.scale_factor`
- `pysc.game.backdrop_index`
