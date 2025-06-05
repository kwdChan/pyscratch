---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---
# Scratch corresponding python functions
---
## Motion
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



## Looks
---
**say/think [text] for N seconds**
- not implemented yet but a work around is provided using extended features (not scratch corresponding)
- will likely be implemented in the future 

**switch costume to [costume]  / next costume**
- `sprite.set_frame(index: int)
- `sprite.next_frame()`
- extended feature: `sprite.set_frame_mode(mode: str)`

**switch backdrop to [backdrop] / next backdrop
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
- ==`pysc.game.show_sprite(sprite)` ==
- ==`pysc.game.hide_sprite(sprite)`==

**go to [front/back] layer**
- `pysc.game.move_to_back(sprite)`
- `pysc.game.bring_to_front(sprite)`

**go \[forward/backward\] \[N\] layers**
- `pysc.game.change_layer_by(sprite, by: int)`
- `pysc.game.change_layer(sprite, layer: int)`

variable access: **costume number, backdrop number, size**
- `sprite.frame_mode`, `sprite.frame_idx`
- `sprite.scale_factor`
- `pysc.game.backdrop_index`


## Sound
**play sound [sound]** ~~until done~~
- `pysc.game.load_sound(key, path)`
- `pysc.game.play_sound(key, volume)`
- no corresponding function to the "until done" part
	- workaround exists

**set/change sound effect**
- no corresponding function. deemed less important. 

**change/set volume**
- no corresponding function but easy workaround exists
- `pysc.game.play_sound(key, volume)`

## Events
In scratch, every stack of code blocks start from an event. An event happens, and the event triggers the code to start running. Without the event on the top, the code blocks will never run. 

In python, the stack of code blocks under the event is put inside a function: 
```python
def my_code_block():
	sprite.move_indir(10)
	sprite.add_rotation(10)
	pysc.game.play_sound('sound1', volume=0.7)
```
This function is known as a event handler. A handlera is any function that are meant to be run by an event. Just like in scratch, the code will not run without having event that triggers the code. This is how you add code to the event in python:
```python
game_start_event = pysc.game.when_game_start()
game_start_event.add_callback(my_code_block)
```

Unlike scratch, some events in python pass on values to the code it triggers. In this case, your callback function need to accept these values as the arguments of the function: 

```python
# this function is meant to be passed to when_key_pressed,
# which passes in two values:
# - key: the key that is being passed
# - updown: key down or key up
def on_key_press(key, updown):
	if key == 'a' and updown == 'down':
		sprite.move_indir(-10)
	if key == 'd' and updown == 'down':
		sprite.move_indir(10)

keypress_event = sprite.when_key_pressed()
keypress_event.add_callback(on_key_press)
```
if your callback function expects any parameter that the event does not pass in, or if your callback function does not expect any parameter that the event passes in, an error will occur.




**when green flag clicked**  
- when_game_start
	- no parameters

**when [key] key pressed**
- when_any_key_pressed
	- two parameters
		- key 
		- updown
	- catch all keys and both up and down
- when_key_pressed(key: str)
	- one parameters
		- updown
**when this sprite clicked**
- when_this_sprite_clicked
	- no parameters

**when backdrop switches to [backdrop]**
- when_backdrop_switched
	- no parameter

- when_any_backdrop_switched
	- one parameter
		- index: the new backdrop index
	- catch all backdrop changes

**when [timer/loudness] > [N]**
- when_timer_above
	- one parameter
		- n: the remaining number of times this event will get triggered (this will always be 0 in this event)

**when I receive [message]** 
- when_receive_message (topic)
- one parameter
	- data: a value of any type passed by the message 

**broadcast [message] ~~and wait~~**
- broadcast_message (topic, )

## Control
**wait N second**
- `yield N`

**repeat N** 
- `for i in range(N): `

**forever**
```python
while True: 
	# whatever
	yield 10
````
**if then else**
```python
if condition:
	pass
else:
	pass
```
**wait until**
```python
while not condition:
	yield 0.1
# whatever
```
**repeat until**
```python
while condition:
	# whatever
	yield 0.1

```
**stop [all/this script/other scripts in sprite]**
- no direct corresponding function
- `event.remove()`
- `sprite.remove()`

**when I start as a clone**
- sprite.when_started_as_clone

**create clone of [sprite]**
- `sprite.clone_myself()` 
- discouraged: sensing function: the touch detection is specific to the individual sprite in python 

**delete this clone**
- sprite.remove()

## Sensing
**touching [mouse-pointer/edge/sprite]**
- `pysc.sensing.is_touching(sprite_a, sprite_b)`
- `pysc.sensing.is_touching_mouse(sprite)`
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

## Operators
Most of the items here need no mentions
Special mentions: 
- `pysc.helper.random_number`
- `pysc.helper.cap`

## Variables
The users are expected to be familiar with the scope of the variables and the difference between redefining a variable and change a variable in place. 
For shared data across the entire program, put the variable in the dictionary: `pysc.game.shared_data`
**Display**
- add the variable to `pysc.game.shared_data`
- `pysc.create_shared_data_display_sprite`



## Adding a sprite to the scene 
**Basic shapes**
- `pysc.create_rect_sprite`
- `pysc.create_circle_sprite`

**Single costume sprite** 
- `pysc.create_single_costume_sprite`

**Animated sprite** (multiple costumes with different mode)
- `pysc.create_animated_sprite`



## Adding backdrops
- `pysc.helper.load_image`
- Optional
	- `pysc.helper.scale_to_fill_screen`
	- `pysc.helper.scale_to_fit_aspect`
	- `pysc.helper.scale_and_tile`
- `game.set_backdrops([background])`

