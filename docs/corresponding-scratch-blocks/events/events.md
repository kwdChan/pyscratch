---
title: Event Functions
parent: Events
nav_order: 1
---
# Events
---

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
