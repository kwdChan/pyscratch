---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: Home
nav_order: 0
---
# Pyscratch
---
This library provides an easy transitioning from Scratch to Python. Scratch-like control plus extended features provided by pymunk. 

There are four functional parts of this library:
- Core functions
- Extended functions
- Asset loading functions
- Ready-to-use assets (Not implemented yet)

These are just different functional parts that serve different purposes. They are separated for project management reason and are they not actual segregated components in the library. 

## Core Functions
A minimal set of functions that is highly analogous to the Scratch blocks for easy transitioning from Scratch to python. It should be possible to "translate" the majority of the Scratch programs into python using the core features with some [exceptions](corresponding-scratch-blocks/exceptions.html).  

The major development of this part of the library is considered completed but small updates and testing is still required. 


## Extended Functions
More powerful and flexible events and functions based on the pymunk physics engine. A lot of the features have been implemented but need to be simplified. 


## Asset Processing Functions 
Before any coding happens, the sprites first need to be created. On Scratch, the users have an GUI to edit sprites, backdrops and sound. This part of the library aids this process. 

The current process of adding sprites, backdrops and sound is now sufficiently simple but still not comparable to Scratch. Looking for ideas to simplify it further. 

Possible new features: 
- Some kinds of scene assembling tools
- Pixel grids to help finding the coordinates for scene design. 
- Save and reload sprite locations 

## Ready-to-use Assets (Not implemented yet)
The coding itself isn't the only challenge in game development. Finding suitable arts on the internet and correctly process them before incorporating them into the game can be a painful process. Some ready-to-use charactors would be very helpful to keep the users motivated. 


Not implemented yet. This will be the main focus of this project right after the documentation is completed. 

