# PyScratch 

PyScratch is a Python game development framework built on top of `pygame` and `pymunk`. It is designed to make it easy to move from **Scratch** to **Python** by providing Scratch‑like building blocks and workflows in a real programming language.

Most Scratch programs can be “translated” into PyScratch with minimal structural changes, making it ideal for teaching, learning, and prototyping games and interactive animations.

For full documentation and examples, see the project website:  
https://kwdchan.github.io/pyscratch/

---

## Video Showcase

**Basic example** — tutorial-style getting started:

<video src="https://pub-c2a3ea7135244e11ad43c1591d006cf0.r2.dev/showcase-video/getting-started.mp4" controls autoplay loop muted width="300"></video>

**Advanced example** — perspective background (scale and move by depth for a 3D-like effect):

<video src="https://pub-c2a3ea7135244e11ad43c1591d006cf0.r2.dev/showcase-video/perspective_background.mp4" controls autoplay loop muted width="300"></video>

For more examples (Pong, Bullet Hell, Doodle Jump, and others), see the [PyScratch documentation site](https://kwdchan.github.io/pyscratch/).

---

## Features

- **Scratch‑style API**
  - High‑level functions and classes analogous to Scratch blocks.
  - Sprites, backdrops, events, messages, and control flow are represented in a familiar way.
  - Enables step‑by‑step “block‑to‑code” translation of Scratch projects.

- **Extended capabilities beyond Scratch**
  - More powerful and flexible functions for advanced users.
  - Events (messages, key presses, etc.) can carry parameters.
  - Sprites and events can be created and destroyed dynamically inside other event handlers.
  - Built on `pygame` and `pymunk`, so you can gradually drop down to lower‑level control when needed.

- **Asset loading & processing**
  - One‑line helpers to load images, animations, sounds, and other assets.
  - Experimental sprite editing tool to slice irregular sprite sheets and preview animations.
  - Sprite locations can be saved and reloaded in one line for quick scene assembly.
  - Optional grid lines and mouse coordinate display on the default background to help with layout.

---

## Who is PyScratch for?

- **Learners** who already know Scratch and want to move into “real code” without losing familiar concepts.
- **Teachers** who want a gentle bridge from block‑based to text‑based programming.
- **Hobbyists and tinkerers** who like Scratch’s model but want Python’s flexibility and ecosystem.

---

## Getting Started

### Installation

```bash
pip install pyscratch-pysc
```

If you use a virtual environment, make sure it is activated before installing.

### Minimal example

```python
import pyscratch as pysc
from pyscratch import game

# create a sprite 
chest = pysc.create_single_costume_sprite("assets/chest-open.png")

# create an event
@chest.when_this_sprite_clicked()
def my_click_event():
    print("I am a chest! ")
    chest.x += 100 # move the chest

# start the game
game.update_screen_mode((1024, 576)) # screensize
game.start(60) # framerate 
```

Check the documentation site for more tutorials and complete examples:  
https://kwdchan.github.io/pyscratch/tutorial/day1-basics/

---

## Scratch‑Corresponding Functionality

PyScratch aims to provide a nearly complete mapping of Scratch concepts into Python:

- **Sprites and backdrops** with positions, costumes, and layers.
- **Events** such as “when game start”, messages, key presses, and collisions.
- **Motion, looks, sound, control, sensing, and variables** with clear, Scratch‑like equivalents.

The goal is that most existing Scratch projects can be ported by translating blocks into equivalent PyScratch calls, without redesigning the overall structure.

---

## Extended Functionality

On top of Scratch‑compatible features, PyScratch adds:

- **Parameterized events** so message and key events can carry data.
- **Dynamic content** so sprites, events, and other objects can be created or removed at runtime from within event handlers.
- **Python power** so you can use the full Python ecosystem while keeping a Scratch‑like conceptual model.

---

## Asset Processing and Development Aids

Creating and managing assets is a big part of building Scratch‑style projects. PyScratch includes helpers to streamline that workflow:

- **One‑line asset loading** for images, sprite sheets, sounds, and backgrounds.
- **Sprite sheet tools** to cut irregular sprite sheets and preview animations.
- **Scene assembly helpers** to save and reload sprite positions with one line of code.
- **Visual aids** such as grid overlays and mouse coordinate readouts to help you position and align sprites.

---

## Change History

### v2.1.0 — 25 Oct 2025
- Events and conditions can now be used as decorators (they can be called directly as a shortcut for `add_handler`).

### v2.0.2 — 22 Oct 2025
- Fixed layering being reset after hide and show.

### v2.0.1 / v2.0.0 — 12 Oct 2025
- **v2.0.1**: Restored backward compatibility for integer‑indexed backdrops from v1.
- **v2.0.0**: Backdrops are now indexed by keys instead of integers.

### v1.0.4 — 12 Sep 2025
- Fixed a show/hide collision issue caused by deferring movement to the frame update.

### v1.0.3 — 07 Sep 2025
- Added missing dependency `Pillow`.
- Specified dependency versions.

### v1.0.0 — Jul 2025
- Initial release.
