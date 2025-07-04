---
title: Events
parent: Corresponding Scratch Blocks
nav_order: 4
---
# Events
---
In scratch, every stack of code blocks start from an event. An event happens, and the event triggers the code to start running. Without the event on the top, the code blocks will never run. 

In python, the stack of code blocks under the event is put inside a function: 
```python
def my_code_block():
	my_sprite.move_indir(10)
	my_sprite.add_rotation(10)
	pysc.game.play_sound('sound1', volume=0.7)
```
This function is known as a event handler. A handler is any function that are meant to be run by an event. Just like in scratch, the code will not run without having event that triggers the code. This is how you add code to the event in python:
```python
event = my_sprite.when_game_start()
event.add_handler(my_code_block)

# or in one line
my_sprite.when_game_start().add_handler(my_code_block)
```

Unlike scratch, some events in python pass on values to the code it triggers. In this case, your handler function need to accept these values as the arguments of the function: 

```python
# this function is meant to be passed to when_any_key_pressed,
# which passes in two values:
# - key: the key that is being passed
# - updown: key down or key up
def on_key_press(key, updown):
	if key == 'a' and updown == 'down':
		sprite.move_indir(-10)
	if key == 'd' and updown == 'down':
		sprite.move_indir(10)

keypress_event = sprite.when_any_key_pressed()
keypress_event.add_handler(on_key_press)
```
if your handler function expects any parameter that the event does not pass in, or if your handler function does not expect any parameter that the event passes in, an error will occur.

