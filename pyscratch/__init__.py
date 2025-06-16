"""
The reference manual is intended to provide technical specifications for the functions in this library. 
If you are new to this library, visit [getting-started](../getting-started/). 
# Namespace
Everything in this library are directly under the pyscratch namespace. 
So for example, you can use `pyscratch.game` to refer to `pyscratch.game_module.game` or `pyscratch.Sprite` to refer to `pyscratch.sprite.Sprite` etc. 

When you do `import pyscratch as pysc`, they become just `pysc.game`, `pysc.Sprite` and `pysc.random_number` etc. 


# Main Objects
You will be mainly interacting of these following types of objects: 
## 1. pyscratch.game_module.game (pysc.game)
This is an object instead a type of objects. This object represents the game itself. 
You use it to start the game, to play sound, change backdrops and make global changes to the game. 
You can also use it to create events, but it is more convenient to create the events from the sprite.

## 2. pyscratch.sprite.Sprite 
The Sprite objects are the objects that represents the sprites in the game.


## 3. pyscratch.event.Event & pyscratch.event.Condition
This is the object you will get when you run `my_event = sprite1.when_game_start()`
The only way you will interact with this object is to add handler functions to it and to remove it. 


## 4. Pygame objects that represents the assets
pygame is another library that this library depends on. 
You only need to interact with these objects when you are loading the assets (for the sprites, backdrops and text styles)

### 4.1. pygame.Surface
A pygame object that represents an image. 
All the images in this library are represented as pygame.Surface objects. 
You can use pyscratch.helper.load_image to load an image for you. 

### 4.2. pygame.font.Font
A pygame object that represent the font (or the style of the text). 
Some functions require the font object to render the text.
To create a font object: 
```python
font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size
```
"""

from .event import *
from .game_module import *
from .helper import *
from .sprite import *
