---
title: Guides
nav_order: 2
---
# General Guide
If you are new to this library, we recommend going through [Getting Started](../getting-started/) before reading this page.

In general, you can think of most the functions in this library to be in one of these two categories: 

1. **Functions that involve loading the assets (i.e. images and sound).** 
These are mainly functions that helps you adding and editing backdrops, sprites and sounds. These functions do not have an analogous Scratch block because Scratch does not use blocks to create the sprites. Fortunately, there are only a handful of these functions and you can go through them quickly here: [Assets Proceessing Functions](../assets-processing-functions/).

2. **Functions that behave like Scratch blocks.** 
Once you have created the sprites and loaded the backdrops and sound, you can control them the same way you do in Scratch. If you know Scratch, then you already know most of these functions. These functions are listed in [Corresponding Scratch Blocks](../corresponding-scratch-blocks/). The majority of the functions in this library are in this category. 

If you are facing difficulties, you may imagine how you would do it in Scratch, and try to "translate" it to Python. 


## Folder Structure
We strongly recommend that your project folder adopt the following structure:
1. All the images, sounds and fonts are put under the `assets` folder
2. Having a `settings.py` that contains all the constant values to be shared across the entire game such as screen dimensions
3. Having a `main.py` that only starts the game and imports all the sprite files
4. Each sprite has its own python file, just like each sprite has its own coding space in Scratch

Refer to [getting started](../getting-started) for more details. 

Here's an example of how the folder should look like:
```
├─ my_awesome_game/
    ├─ pyscratch/
    ├─ assets/
    ├─ settings.py
    ├─ main.py
    ├─ sprite1.py
    ├─ sprite2.py
    ├─ sprite3.py
    ...
```

In addition, there should be no imports between different sprite files (i.e. do not do `import sprite1` in `sprite2.py` or vice versa) to avoid circular import that is not allowed in Python. This also prevent a complicated chain of dependency between the sprite files. The reference of another sprite should be done using `pysc.game.shared_data`. Follow [this guide](../getting-started/6-reference-other-sprite) for more details. 


