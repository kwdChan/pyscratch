---
title: Control
parent: Corresponding Scratch Blocks
nav_order: 5
---
# Control
---
**wait N second**
- `yield N`

**repeat N** 
- `for i in range(N): `

**forever**

```python
while True: 
    # whatever
    yield 10
```
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

