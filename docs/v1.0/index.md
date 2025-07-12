---
layout: home
title: Home
nav_order: 0
---
# PyScratch

PyScratch is a Python game development framework built on top of Pygame and Pymunk. This library is designed to provide an easy transitioning from Scratch to Python. Scratch analogous functionalities are provided so most Scratch programs can be written using PyScratch without any structural changes.
 
This library focuses on three main areas:
- Providing *nearly* complete Scratch functionality
- Extending Scratch features for the more advanced capabilities  
- Supporting asset loading and processing

## Scratch Corresponding Functionalities
A minimal set of functions that is highly analogous to the Scratch blocks for easy transitioning from Scratch to python. It should be possible to "translate" the majority of the Scratch programs into Python using the core features. 


## Extended Functionalities
The more advance capabilities are provided by: 
- More powerful and flexible functions
- Some events such as messages and key presses can take parameters
- Events and sprites can be created and removed within other events


## Asset Processing and Other Development Aids 
Before coding happens, the sprites first need to be created. On Scratch, the users have an GUI to edit the sprites, backdrops and sound. This part of the library aids this process. The currently implemented features include: 
- One-line functions to load the assets 
- A experimental sprite editing tool for cutting irregular sprite sheets and animation preview 
- Sprite locations can be saved and reloaded in one line for scene assembling
- Grid lines and mouse coordinates on the default background 



## Showcase
<div class="card-container">
  <div class="card">
  <video autoplay loop muted playsinline>
      <source src="media/perspective_background.mp4" type="video/mp4">
      Your browser does not support the video tag.
  </video>  
  <a class="card_link" href="http://justinbieber.com">
  <div class="card-body">
    <p class="card-title">Perspective Background</p>
    <p class="card-text">Scale and move the trees based on the depth and the viewing position to achieve a 3D-like effect. </p>
  </div>
  </a>

</div>
<div class="card">
 
  <video autoplay loop muted playsinline style="max-height: 100%;">
      <source src="media/bullet_hell.mp4" type="video/mp4">
      Your browser does not support the video tag.
  </video>  
  
  
  <div class="card-body">
    <p class="card-title">Bullet Hell</p>
    <p class="card-text">Create sprites and events within events to program complex behaviours. Also notice the </p>
  </div>
</div>

<div class="card">
 
  <video autoplay loop muted playsinline style="max-height: 100%;">
      <source src="media/doodle_jump.mp4" type="video/mp4">
      Your browser does not support the video tag.
  </video>  
  
  
  <div class="card-body">
    <p class="card-title">Partial Recreation of Doddle Jump</p>
    <p class="card-text"> Offset the platform height with the viewing height and use a sprite with 100% transparency to detect the feet touching the platform. </p>
  </div>
</div>
</div>

