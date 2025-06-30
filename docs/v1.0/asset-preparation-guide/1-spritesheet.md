---
title: Handling Sprite Sheet
parent: Graphic Asset Preparation
nav_order: 4
---

Two tools 
- PyScratch Sprite Editor 
- Piskel




Piskel
- A animation editor for pixel arts
- Allows you to draw
- Allows you to cut sprite sheets (good for small sprite sheets)


PyScratch Sprite Editor 
- Aims to complement the functionality of piskel
- Allows you cut sprite sheets and select the frames into different animations
- Plan to allow you to select single images 
- Plan to allow merging frame for irregular sprite sheets
- Need to be better at working with large sprite sheet
- 


Sprite sheet (SS) segmentation tool 
- fit the best line == fit the best offset (a button to do so) (okay)
    - cut the least amount of continus pixel / multiple of empty space cycles 
    - ~~most centered sprites sparse sprite sheets?~~

- fit the number of columns and rows (a button to do so) 
    - okay for pixel size fitting
    - fitting the number of columns or rows require certainty in the total pixel size

- merge frames
    - auto detect merged frames 
    - split on right click

- solve the kenney fish background problem
    - only the column/rows are certain
    - the total number of pixel are not certain
    - the frame pixel size are not certain 
    - the offset are not certain
    - goal: find the best cut
    - same problem arise in very sparse SS
        - i assume it's a non-issue if the frames are on the edge of the SS 
        - but what if it's in the middle of the ss and cutting is necessary? 

- save the cut frames into a folder
- load all frames at once 

Add single images
Scroll to scale every where
Drag to pan every where 


Adjust the relative position and scale of the frame
