---
title: Font
parent: Other Gudies
nav_order: 99
---
# Font

Fonts are used to render text. As of version 1.0, fonts are only used by
<a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.write_text">Sprite.write_text</a>. 

To write any text in the game, you will need to create a pygame font object and pass it to Sprite.write_text. 
```python
import pyscratch as pysc
import pygame

# Create the font. For more details, see: https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
default_font = pygame.font.SysFont(None, size=48)  # None for the default font

# create the sprite
colour = (127, 127, 127)
width, height = 20, 20
sprite = pysc.create_rect_sprite(colour, width, height)

# write the text on the sprite
sprite.write_text("hello!", default_font)
```

You can choose other font by specifying name of the font in `pygame.font.SysFont`.
You can also download other fonts from the asset library and load it using `pygame.font.Font`.
**However, as of 29 Jun 2025, only the default font has been tested and other fonts are not guaranteed to work.**