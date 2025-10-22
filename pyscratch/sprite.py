"""
Everything in this module is directly under the pyscratch namespace. 
For example, instead of doing `pysc.sprite.create_animated_sprite`,
you can also directly do `pysc.create_animated_sprite`.
"""



from __future__ import annotations
from enum import Enum
from functools import cache
import inspect
from typing import Any, Callable, Dict, Hashable, Iterable, List, Optional, ParamSpec, Tuple, Union, cast, override
from typing_extensions import deprecated


import numpy as np
import pygame 
import pymunk

import pyscratch.game_module
from .game_module import Game, game
from .helper import adjust_brightness, set_transparency, create_rect, create_circle, load_frames_from_folder, load_gif_frames, load_frames_from_gif_folder
from pathlib import Path


def create_sprite_from_gif(path,  *args, **kwargs):

    """
    Create a sprite using a GIF file or GIF files inside a folder.

    The folder should be organised in the following way: 
    ```
    ├─ player/
        ├─ walking.gif
        ├─ idling.gif
        ├─ jumping.gif
        ...
    ```
    **Example**
    ```python
    # takes the path of a gif (single animation sprite)
    my_sprite1 = create_sprite_from_gif("assets/player/walking.gif") 
    
    # takes the path of the folder (multiple animations)
    my_sprite2 = create_sprite_from_gif("assets/player") 
    ```
    """


    path = Path(path)

    if path.is_dir():
        frame_dict = load_frames_from_gif_folder(path)
    else:
        frames = load_gif_frames(path)
        frame_dict = {'always': frames}
    return Sprite(frame_dict, *args, **kwargs)
    
    
    

def create_animated_sprite(folder_path,  *args, **kwargs):
    """
    Create a sprite using the images inside a folder. 

    The folder should be organised in one of these two ways: 

    **Option 1**: Only one frame mode. *Note that the images must be numbered.*
    ```
    ├─ player/
        ├─ 0.png
        ├─ 1.png
        ├─ 2.png
        ...
    ```

    **Option 2**: Multiple frame modes. *Note that the images must be numbered.*
    ```
    ├─ player/  
        ├─ walking/  
            ├─ 0.png  
            ├─ 1.png  
            ...
        ├─ idling/
            ├─ 0.png
            ├─ 1.png
            ... 
        ...
    ``` 


    **Example**
    ```python
    # takes the path of the folder 
    my_sprite1 = create_animated_sprite("assets/player") 
    
    # optionally take in whatever parameters that the `Sprite` constructor take. 
    my_sprite2 = create_animated_sprite("assets/player", position=(200, 200)) 
    
    # For option 2 only: optionally set the `starting_animation` parameter in the `Sprite` constructor, but it'd still be fine without it.
    my_sprite3 = create_animated_sprite("assets/player", "idling")
    

    # Event: to animate the sprite
    def animating():
    
        # switch to the next frame every 0.2 second
        while True: 
            my_sprite1.next_frame() # scratch block: next costume
            yield 0.2

    my_sprite1.when_game_start().add_handler(animating)


    # if doing option 2: use `set_animation` to select the frame
    # there's no equivalent scratch block
    def movement():
        while True: 
            if pysc.sensing.is_key_pressed('right'): 
                my_sprite1.set_animation('walking') # reference to the folder name
                my_sprite1.x += 1
            else:
                my_sprite1.set_animatione('idling') 
            
            yield 1/FRAMERATE

    my_sprite1.when_game_start().add_handler(movement)

    ```
    Parameters
    ---
    folder_path: str
        The path of the folder that contains the images

    \\*args & \\*\\*kwargs: Optional
        Whatever the `Sprite` constructor takes, except the `frame_dict` parameter.
    """
    frame_dict = load_frames_from_folder(folder_path)
    return Sprite(frame_dict, *args, **kwargs)


def create_single_costume_sprite(image_path, *args, **kwargs):
    """
    Create a sprite with only one costume, given the path to the image
    
    Example
    ```python
    my_sprite1 = create_single_costume_sprite("assets/player.png")

    # Optionally pass some parameters to the `Sprite` constructor
    my_sprite2 = create_single_costume_sprite("assets/player.png", position=(200, 200)) 
    
    ```
    Parameters
    ---
    image_path: str
        The path of the images

    \\*args & \\*\\*kwargs: Optional
        Whatever the `Sprite` constructor takes, except `frame_dict` & `starting_animation`.
    """
    img = pygame.image.load(image_path).convert_alpha()
    frame_dict = {"always": [img]}
    return Sprite(frame_dict, "always", *args, **kwargs)


def create_shared_data_display_sprite(key, font:Optional[pygame.font.Font]=None, size = (150, 50), bg_colour=(127, 127, 127), text_colour=(255,255,255), position: Optional[Tuple[float, float]]=None, update_period=0.1, **kwargs):
    """
    Create a display for a variable inside shared_data given the dictionary key (i.e. the name of the variable). 
    The variable display will update every `update_period` seconds.
    The variable display is created as a sprite. 

    This function is created using only basic pyscratch functions and events. 
    If you want a more customised display, you may want to have a look at the source code as an example how it's done.

    Example
    ```python
    
    # if the font is shared by multiple sprites, consider putting it in `settings.py`
    font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size

    # the shared data
    game.shared_data['hp'] = 10
    
    # the variable display is created as a sprite 
    health_display = create_shared_data_display_sprite('hp', font, position=(100, 100), update_period=0.5)
    
    ```
    Parameters
    ---
    key: str
        The dictionary key of the variable in `game.shared_data` that you want to display.
    font: None or pygame.font.Font
        The pygame font object. Refer to the website of pygame for more details.
        If None, a default font will be used. 
    size: Tuple[float, float]
        The size of the display panel
    bg_colour: Tuple[int, int, int] or Tuple[int, int, int, int] 
        The colour of the display panel in RGB or RGBA. Value range: [0-255]
    text_colour: Tuple[int, int, int] or Tuple[int, int, int, int] 
        The colour of the text in RGB or RGBA. Value range: [0-255]
    position: Tuple[int, int] 
        The position of the display
    update_period: float
        The variable display will update every `update_period` seconds.
    \\*\\*kwargs: Optional
        Whatever the `Sprite` constructor takes, except `frame_dict`,`starting_animation` & `position`
    """

    if font is None:
        font = pygame.font.Font(None, 36)

    w, h = size
    if position is None:
        position = w/2+25, h/2+25
    sprite = create_rect_sprite(bg_colour, w, h, position=position, **kwargs)

    def update_value():
        while True: 
            sprite.write_text(f"{key}: {game.shared_data[key]}", font=font, colour=text_colour, offset=(w/2, h/2))
            yield update_period

    sprite.when_game_start().add_handler(update_value)
    return sprite

def create_circle_sprite(colour, radius:float, *args, **kwargs):
    """
    Create a circle sprite given the colour and radius
    Also optionally takes in any parameters that the `Sprite` constructor takes, except `frame_dict` and `starting_animation`

    Example
    ```python
    green_transparent = (0, 255, 0, 127)
    my_rect_sprite = create_rect_sprite(green_transparent, radius=10)
    ```

    Parameters
    ---
    colour: Tuple[int, int, int] or Tuple[int, int, int, int]
        The colour of the rectangle in RGB or RGBA. Value range: [0-255].
    radius: float
        the radius of the cirlce.
    \\*args & \\*\\*kwargs: Optional
        Whatever the `Sprite` constructor takes, except `frame_dict` & `starting_animation`.
    """

    circle = create_circle(colour, radius)
    return Sprite({"always":[circle]}, "always", *args, **kwargs)


def create_rect_sprite(colour, width, height, *args, **kwargs):
    """
    Create a rectanglar sprite given the colour, width and height
    Also optionally takes in any parameters that the `Sprite` constructor takes, except `frame_dict` and `starting_animation`

    Example
    ```python
    green_transparent = (0, 255, 0, 127)
    my_rect_sprite = create_rect_sprite(green_transparent, width=10, height=20)
    ```

    Parameters
    ---
    colour: Tuple[int, int, int] or Tuple[int, int, int, int]
        The colour of the rectangle in RGB or RGBA. Value range: [0-255].
    width: float
        the width (x length) of the rectangle.
    height: float
        the height (y length) of the rectangle.
    \\*args & \\*\\*kwargs: Optional
        Whatever the `Sprite` constructor take, except `frame_dict` & `starting_animation`.
    """
    rect = create_rect(colour, width, height)
    return Sprite({"always":[rect]}, "always", *args, **kwargs)


def create_edge_sprites(edge_colour = (255, 0, 0), thickness=4, collision_type=1):
    """
    A convenience function to create the top, left, bottom and right edges as sprites

    Usage
    ```python
    # consider putting the edges in settings.py
    top_edge, left_edge, bottom_edge, right_edge = create_edge_sprites()
    ```
    """
    
    # TODO: make the edge way thicker to avoid escape due to physics inaccuracy 
    # edges
    screen_w, screen_h = game._screen.get_width(), game._screen.get_height()

    real_thickness = 300 + thickness

    top_edge = create_rect_sprite(edge_colour, screen_w, real_thickness, (screen_w/2, -real_thickness/2+thickness), body_type= pymunk.Body.STATIC)
    
    bottom_edge = create_rect_sprite(edge_colour, screen_w, real_thickness, (screen_w/2, screen_h+real_thickness/2-thickness),body_type= pymunk.Body.STATIC)
    
    left_edge = create_rect_sprite(edge_colour, real_thickness, screen_h, (-real_thickness/2+thickness, screen_h/2),body_type= pymunk.Body.STATIC)
    
    right_edge = create_rect_sprite(edge_colour, real_thickness, screen_h, (screen_w+real_thickness/2-thickness,  screen_h/2),body_type= pymunk.Body.STATIC)

    top_edge.set_collision_type(collision_type)
    bottom_edge.set_collision_type(collision_type)
    left_edge.set_collision_type(collision_type)
    right_edge.set_collision_type(collision_type)

    return top_edge, left_edge, bottom_edge, right_edge



class _RotationStyle(Enum):
    ALL_AROUND = 0
    LEFTRIGHT = 1
    FIXED = 2


_FrameDictType = Dict[str, List[pygame.Surface]]
class _DrawingManager:
    def __init__(self, frame_dict, starting_animation):

        
        self.frame_dict_original: _FrameDictType = {k: [i.copy() for i in v] for k, v in frame_dict.items()} # never changed
        self.frame_dict: _FrameDictType = {k: [i.copy() for i in v] for k, v in frame_dict.items()} # transformed on the spot
        

        self.animation_name = starting_animation
        self.frames = self.frame_dict[self.animation_name]
        self.frame_idx: int = 0

        # transforming parameters -> performed during update, but only when the transform is requested
        self.request_transform = False
        self.transparency_factor = 1.0
        self.brightness_factor = 1.0
        self.scale_factor: float = 1.0
        self.rotation_offset: float # TODO: to be implemented

        def create_blit_surfaces():
            blit_surfaces = {}
            for k in self.frame_dict_original:
                for i in range(len(self.frame_dict_original[k])):
                    blit_surfaces[(k, i)] = []
            return blit_surfaces
        self.blit_surfaces: Dict[Tuple[str, int], List[Tuple[pygame.Surface, Tuple[float, float]]]] = create_blit_surfaces()


        # rotation and flips -> performed every update on the current frame
        self.rotation_style: _RotationStyle = _RotationStyle.ALL_AROUND
        self.flip_x: bool = False
        self.flip_y: bool = False
        self.mask_threshold: int = 1


    def set_mask_threshold(self, value=1):
        self.mask_threshold = value

    def set_rotation_style(self, flag: _RotationStyle):
        self.rotation_style = flag

    def flip_horizontal(self, to_flip:bool):
        self.flip_x = to_flip

    def flip_vertical(self, to_flip:bool):
        self.flip_y = to_flip

    def set_animation(self, new_mode):
        if new_mode == self.animation_name:
            return 
        self.animation_name = new_mode
        self.frames = self.frame_dict[new_mode]
        self.frame_idx = 0

    def set_frame(self, idx):
        # also allow direct setting of frame_idx
        self.frame_idx = idx

    def next_frame(self):
        self.frame_idx = (self.frame_idx+1) % len(self.frames)

    # core transform requests 
    def set_scale(self, factor):
        if not self.scale_factor == factor:
            self.request_transform = True
            self.scale_factor = factor
            return True
        else:
            return False


    def set_brightness(self, factor):
        self.brightness_factor = factor
        self.request_transform = True

    def set_transparency(self, factor):
        self.transparency_factor = factor
        #self.request_transform = True

    def blit_persist(self, surface: pygame.Surface, offset=(0,0), centre=True, reset=True):
        w, h = surface.get_width(), surface.get_height()
        if centre:
            offset = (offset[0]-w/2, offset[1]-h/2)
        if reset: 
            self.blit_surfaces[(self.animation_name, self.frame_idx)] = [(surface, offset)]
        else: 
            self.blit_surfaces[(self.animation_name, self.frame_idx)].append((surface, offset))
        self.request_transform = True
        
    # transform related helper
    def scale_by(self, factor):
        self.set_scale(self.scale_factor*factor)

    def write_text(self, text: str, font: pygame.font.Font, colour=(255,255,255), offset=(0,0), centre=True, reset=True):
        text_surface = font.render(text, True, colour) 
        self.blit_persist(text_surface, offset, centre, reset)

    # transform
    #@cache
    def transform_frames(self):
        self.request_transform = False
        for k, frames in self.frame_dict_original.items():
            new_frames = []
            for idx, f in enumerate(frames):
                f_new = f.copy()
                for s, o in self.blit_surfaces[(k, idx)]:
                    f_new.blit(s, o)
                #f_new = set_transparency(f_new, self.transparency_factor)
                f_new = adjust_brightness(f_new, self.brightness_factor)
                f_new = pygame.transform.scale_by(f_new, self.scale_factor)
                new_frames.append(f_new)

            self.frame_dict[k] = new_frames
            
        self.frames = self.frame_dict[self.animation_name]

    def on_update(self, x, y, angle) -> Tuple[pygame.Surface, pygame.Rect, pygame.Mask]:
        if self.request_transform:
            self.transform_frames()

        img = self.frames[self.frame_idx]

        if self.rotation_style == _RotationStyle.ALL_AROUND: 
            img = pygame.transform.rotate(img, -angle)
    
        elif self.rotation_style == _RotationStyle.LEFTRIGHT:
            if angle > -90 and angle < 90:
                pass
            else:
                img = pygame.transform.flip(img, True, False)
             
        elif self.rotation_style == _RotationStyle.FIXED:
            pass

        img = pygame.transform.flip(img, self.flip_x, self.flip_y)


        img_w, img_h = img.get_width(), img.get_height()
        rect = img.get_rect(
            center=(x, y),
              width=img_w,
              height=img_h,
              )
        
        
        mask = pygame.mask.from_surface(img, self.mask_threshold)
        img = set_transparency(img, self.transparency_factor)

        return img, rect, mask 

class ShapeType(Enum):
    """@private"""
    BOX = 'box'
    CIRCLE = 'circle'
    CIRCLE_WIDTH = 'circle_width'
    CIRCLE_HEIGHT = 'circle_height'
    

class _PhysicsManager:
    def __init__(self, game, body_type, shape_type, shape_size_factor, position, initial_image):

        # shape properties that requires shape changes
        self.shape_type: ShapeType = shape_type
        self.collision_type: int = 1
        self.shape_size_factor: float = shape_size_factor

        # shape properties that does not require shape changes
        self.elasticity: float = 1.0
        self.friction: float = 0

        # update
        self.__request_shape_update = False

        # core variables
        self.game = game
        self.space = game._space

        self.body =  pymunk.Body(1, 100, body_type=body_type)
        self.body.position = position
        self.shape = self.create_new_shape(initial_image)

        self.space.add(self.body, self.shape)   



    def request_shape_update(self):
        self.__request_shape_update = True

    def set_shape_type(self, shape_type: ShapeType):
        if shape_type == self.shape_type:
            return 
        self.shape_type = shape_type 
        self.__request_shape_update = True     

    def set_shape_size_factor(self, shape_size_factor: float):
        if shape_size_factor == self.shape_size_factor:
            return 
        self.shape_size_factor = shape_size_factor 
        self.__request_shape_update = True     


    def set_collision_type(self, collision_type):
        if collision_type == self.collision_type:
            return 
        self.collision_type = collision_type 
        self.__request_shape_update = True
    
    def create_new_shape(self, image: pygame.Surface):
        rect = image.get_rect()
        width = rect.width*self.shape_size_factor
        height = rect.height*self.shape_size_factor
        
        if self.shape_type == ShapeType.BOX: 
            new_shape = pymunk.Poly.create_box(self.body, (width, height))

        elif self.shape_type == ShapeType.CIRCLE:
            radius = (width+height)//4
            new_shape = pymunk.Circle(self.body,radius)

        elif self.shape_type == ShapeType.CIRCLE_WIDTH:
            new_shape = pymunk.Circle(self.body, rect.width//2)

        elif self.shape_type == ShapeType.CIRCLE_HEIGHT:
            new_shape = pymunk.Circle(self.body, height//2)
        else:
            raise ValueError('invalid shape_type')
        
        new_shape.collision_type = self.collision_type
        new_shape.elasticity = self.elasticity 
        new_shape.friction = self.friction 


        return new_shape


    def on_update(self, image: pygame.Surface):
        
        if self.__request_shape_update: 
            self.__request_shape_update = False

            new_shape = self.create_new_shape(image)

            game._cleanup_old_shape(self.shape)
            self.space.remove(self.shape)

            self.shape = new_shape
            self.space.add(self.shape)         


# Creating Sprite contruction function outside this file will make the automatic sprite ID assignment much less helpful
class Sprite(pygame.sprite.Sprite):
    """
    Objects of the Sprite class represents a sprite.
    """
    def __init__(
            self, 
            frame_dict: Dict[str, List[pygame.Surface]], 
            starting_mode:Optional[str]=None, 
            position= (100, 100), 
            identifier:Optional[str]=None, 
            shape_type = ShapeType.BOX, 
            shape_size_factor=1.0, 
            body_type=pymunk.Body.KINEMATIC, 
        ):
        """
        You might not need to create the sprite from this constructor function. 
        **Consider functions like `create_single_costume_sprite` or `create_animated_sprite`
        as they would be easier to work with.**

        Example:
        ```python
        image1 = helper.load_image("assets/image1.png")
        image2 = helper.load_image("assets/image2.png")
        image3 = helper.load_image("assets/image3.png")
        image4 = helper.load_image("assets/image4.png")

        frame_dict = {"walking": [image1, image2], "idling": [image3, image4]}
        my_sprite = Sprite(frame_dict, "walking", shape_type="circle", body_type=pymunk.Body.DYNAMIC)
        
        # alternative (exactly the same)
        my_sprite = Sprite(frame_dict, "walking", shape_type=ShapeType.CIRCLE, body_type=pymunk.Body.DYNAMIC)
        ```

        Parameters
        ---
        frame_dict: Dict[str, List[pygame.Surface]]
            A dictionary with different frame modes (str) as the keys 
            and lists of images as the values 

        starting_mode:Optional[str]
            The starting frame mode. If not provided, 
            any one of the frame mode might be picked 
            as the starting frame mode.

        position: Tuple[float, float]
            The starting position of the sprite.

        identifier: Optional[str]
            Used for identifying the sprite for loading sprite states (position and direction).
            Each sprite should have unique identifier.
            Put to None for automatic assignment based on the file name and the order of creation. 

        ~~shape_type: ShapeType~~
            *FEATRUE UNDER DEVELOPMENT. LEAVE AS DEFAULT.*  
            The collision shape. See `set_shape` for more details.

        ~~shape_size_factor: float~~
            *FEATRUE UNDER DEVELOPMENT. LEAVE AS DEFAULT.*   

        ~~body_type: int~~
            *FEATRUE UNDER DEVELOPMENT. LEAVE AS DEFAULT.*  
            The pymunk body type. Leave out the parameter if unsure. 
            Can be `pymunk.Body.KINEMATIC`, `pymunk.Body.DYNAMIC` or `pymunk.Body.STATIC` 
            - Use kinematic if you want the sprite to move when when you tell it to. 
            - Use dynamic if you want the sprite to be freely moving by physics. Also refer to `set_collision_type` to enable collision.  
            - Use static if you do not want it to move at all. 
        """
        super().__init__()

        self.image: pygame.Surface # rotated and flipped every update during self.update
        "@private"
        self.rect: pygame.Rect # depends on the rotated image and thus should be redefined during self.update
        "@private"

        if starting_mode is None:
            starting_mode = next(iter(frame_dict))

        self._drawing_manager = _DrawingManager(frame_dict, starting_mode)
        _initial_frame = frame_dict[starting_mode][0]
        self._physics_manager = _PhysicsManager(game, body_type, shape_type, shape_size_factor, position,_initial_frame)
        self.__physics_enabled = False
        self.sprite_data = {}
        """
        A dictionary similar to `game.shared_data`. 

        The access of the items can be done directly through the sprite object. 
        For example, `my_sprite['my_data'] = "hello"` is just an alias of `my_sprite.sprite_data['my_data'] = "hello"` 
        
        You can put any data or variable that should belong to the individuals sprite. 
        A good example would be the health point of a charactor. 

        Let say if you have a uncertain number of enemy in game created by cloning or otherwise, 
        it would be messy to put the health point of each enemy to `game.shared_data`. In this 
        case, putting the health point in the private data is a better choice.


        Example:
        ```python
        # same as `my_sprite.sprite_data['hp'] = 10`
        my_sprite['hp'] = 10

        def on_hit(damage):
            my_sprite['hp'] -= damage

            print("how much hp I have left: ", my_sprite['hp']) 

        my_sprite.when_received_message('hit').add_handler(on_hit)
        
        game.broadcast_message('hit', 2)
        ```
        """

        self._mouse_selected = False
        self.__is_dragging = False
        self.draggable:bool = False
        """Whether or not this sprite is draggable."""


        self.oob_limit: float = 500
        """The sprite will be removed automatically when it is out of the screen for more than `oob_limit` pixel. Default to 500."""


        self._lock_to_sprite = None
        self._lock_offset = 0, 0
        self.__x, self.__y = self._physics_manager.body.position[0],  self._physics_manager.body.position[1]


        self.__direction: pymunk.Vec2d = self._body.rotation_vector     
        self.__rotation_style = _RotationStyle.ALL_AROUND

        self.__removed:bool = False
        self._layer = 1



        # get the caller name
        frame = inspect.currentframe()
        assert frame

        this_file = frame.f_code.co_filename

        while True:
            frame = frame.f_back
            if not frame:
                caller_file = "UNKNOWN"
                break

            caller_file = frame.f_code.co_filename
            #print(caller_file)
            if not caller_file == this_file:
                break


        self._intend_to_show = True
        self._shown = False
        self.hide()
        
        count = game._add_sprite(self, caller_file=caller_file)
        
        self.update()
        self.show()


        self.identifier: str
        """
        An identifier of the sprite for loading sprite states (position and direction).
        Each sprite should have unique identifier.
        Put to None for automatic assignment based on the file name and the order of creation.  
        
        """

        if not identifier: 

        
            self.identifier = caller_file + ":" + str(count) 
        else:
            self.identifier = identifier
            

        #print(self)

    def __repr__(self):
        return f"Sprite(id='{self.identifier}')"
        

    def __getitem__(self, key):
        return self.sprite_data[key]
    
    def __setitem__(self, k, v):
        self.sprite_data[k] = v

    @property
    def _body(self):
        return self._physics_manager.body    
    
    @property
    def _shape(self):
        return self._physics_manager.shape    

    @override
    def update(self):
        "@private"

        if self._lock_to_sprite:
            self._body.position = self._lock_to_sprite._body.position + (self.__x, self.__y) + self._lock_offset 
            self._body.velocity = 0, 0 

        x, y = self._body.position
        self.image, self.rect, self.mask = self._drawing_manager.on_update(x, y, self.__direction.angle_degrees)
        self._shown = self._intend_to_show

        self._physics_manager.on_update(self.image)

        
        if self.__is_dragging:
            self._body.velocity=0,0 
            # TODO: should be done every physics loop or reset location every frame
            # or can i change it to kinamatic temporarily

    def _is_mouse_selected(self):
        # TODO: why did i do this 
        return self._mouse_selected
    
    @property
    def removed(self,) -> bool:
        """Indicates whether or not this sprite has been removed. """
        return self.__removed
    
    
    def set_draggable(self, draggable):
        """
        Set whether or not this sprite is draggable.

        Example: 
        ```python
        # Make the sprite draggable
        my_sprite.set_draggable(True)
        ```
        """
        self.draggable = draggable

    def _set_is_dragging(self, is_dragging):
        self.__is_dragging = is_dragging


    # START: motions   
    @property
    def x(self):
        """
        The x position of the sprite.
        You can change this property to change the x position of the sprite. 

        Remember that the top-left corner is (x=0, y=0), 
        and x increases as the sprite goes right. 

        so setting x to 0 sends the sprite to the left edge. 

        Example: 
        ```python
        # moves the sprite 10 pixels to the right
        my_sprite.x += 10 
        ```
        """
        if self._lock_to_sprite: 
            return self.__x        
        return self._body.position[0]
    
    @property
    def y(self):
        """
        The y position of the sprite.
        You can change this property to change the y position of the sprite. 
        
        Remember that the top-left corner is (x=0, y=0), 
        and y increases as the sprite goes ***down***. 

        so setting y to 0 sends the sprite to the top edge.         

        Example: 
        ```python
        # moves the sprite 10 pixels down
        my_sprite.y += 10 
        ```
        """
        if self._lock_to_sprite: 
            return self.__y
        return self._body.position[1]
    
    @property
    def direction(self):
        """
        The direction of movement of the sprite. 
        Also rotates the sprite image depending on the rotation style.
        You can change this property to change the direction of movement of the sprite. 

        - 0 degree is pointing to the left 
        - 90 degree is pointing ***down***
        - 180 degree is pointing to the right
        - -90 degree or 270 degree is pointing up 

        Therefore, increasing this value turns the sprite clockwise
    
        (If you find it strange that 90 degree is pointing down, 
        it is because y is positive when going down)

        Example: 
        ```python
        # moves the sprite 10 degrees clockwise
        my_sprite.direction += 10 
        ```        
        """

        #self.__direction
        if self.__rotation_style == _RotationStyle.ALL_AROUND:
            return self._body.rotation_vector.angle_degrees
        else: 
            return self.__direction.angle_degrees
   
    @x.setter
    def x(self, v):
        if self._lock_to_sprite: 
            self.__x = v
        else: 
            self._body.position =  v, self._body.position[1]
        
    
    @y.setter
    def y(self, v):
        if self._lock_to_sprite: 
            self.__y = v
        else: 
            self._body.position = self._body.position[0], v

    @direction.setter
    def direction(self, degree):
        if self.__rotation_style == _RotationStyle.ALL_AROUND:
            self._body.angle = degree/180*np.pi

        self.__direction = pymunk.Vec2d.from_polar(1, degree/180*np.pi) 
        #print(self.__direction)


    def _assign_layer(self, layer):
        self._layer = layer


    def move_indir(self, steps: float, offset_degrees=0):
        """
        Moves the sprite forward along `direction + offset_degrees` degrees.

        Example: 
        ```python
        # move along the direction 
        my_sprite.move_indir(10)

        # move along the direction + 90 degrees
        my_sprite.move_indir(10, 90)        
        ```        
        """
        #self._body.position += 
        
        xs, ys = self.__direction.rotated_degrees(offset_degrees)*steps
        self.x += xs
        self.y += ys
        
    # def move_across_dir(self, steps: float, offset_degrees=0):
    #     """
    #     Moves the sprite forward along `direction` + 90 degrees  
    #     """
    #     xs, ys = self.__direction.rotated_degrees(offset_degrees)*steps
    #     self.x += xs
    #     self.y += ys        
        

    def move_xy(self, xy: Tuple[float, float]):
        """
        Increments both x and y. 

        Example: 
        ```python
        # increase x by 10 and decrease y by 5
        my_sprite.move_xy((10, -5))
        ```
        """
        self.x += xy[0]
        self.y += xy[1]

    def set_xy(self, xy: Tuple[float, float]):
        """
        Sets the x and y coordinate. 

        Example: 
        ```python
        # put the sprite to the top-left corner
        my_sprite.set_xy((0, 0))
        ```
        """        
        self.x, self.y = xy


    def distance_to(self, position: Tuple[float, float]) -> float:
        """
        Gets the distance from the centre of this sprite to a location. 

        Example: 
        ```python   
        # returns the distance to the centre of the screen
        distance_to_centre = my_sprite.distance_to((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        ```
        """   
        return (position - self._body.position).length

    def distance_to_sprite(self, sprite: Sprite)-> float:
        """
        Gets the distance between the centres of two sprites. 
        Returns one float or a tuple of two floats. 

        Example: 
        ```python   
        # returns the distance to another sprite
        distance_to_centre = my_sprite.distance_to_sprite(my_sprite2)
        ```
        """  

        return self.distance_to(sprite._body.position)
    

    def point_towards(self, position: Tuple[float, float], offset_degree=0):
        """
        Changes the direction to point to a location. 

        Example: 
        ```python   
        # point to the centre of the screen
        my_sprite.point_towards((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        ```
        """          

        
        rot_vec = (position - self._body.position).normalized()
        self.direction = (rot_vec.angle_degrees + offset_degree) 


    def point_towards_sprite(self, sprite: Sprite, offset_degree=0):
        """
        Changes the direction to point to a sprite. 

        Example: 
        ```python   
        # point to another sprite
        my_sprite.point_towards_sprite(another_sprite2)
        ```
        """  
        self.point_towards(sprite._body.position, offset_degree)

    def point_towards_mouse(self, offset_degree=0):
        """
        Changes the direction to point to the mouse. 

        Example: 
        ```python   
        # point to the mouse
        my_sprite.point_towards_mouse()
        ```
        """  
        self.point_towards(pygame.mouse.get_pos(), offset_degree)


    def if_on_edge_bounce(self, bounce_amplitude=5):
        """
        Works very similarly to the Scratch counterpart except that it still allows the sprite to go into the edge if you force it to. 

        The optional parameter `bounce_amplitude` is used for specifying by how much the sprite should be repelled from the edge.
        """
        if self._lock_to_sprite:
            print("a locked sprite cannot bounce")
            return
        
        x, y = self.__direction
        changed = False

        if self.is_touching(game._top_edge):
            changed = True
            self.y += bounce_amplitude
            y = abs(y)

        elif self.is_touching(game._bottom_edge):
            changed = True
            self.y -= bounce_amplitude
            y = -abs(y)
        
        if self.is_touching(game._left_edge):
            changed = True
            self.x += bounce_amplitude
            x = abs(x)

        elif self.is_touching(game._right_edge):
            changed = True
            self.x -= bounce_amplitude
            x = -abs(x)

        # is it really gonna make a difference in the performance?
        if changed: 
            self.direction = pymunk.Vec2d(x, y).angle_degrees

    def retrieve_saved_state(self, not_exist_ok=True) -> bool:
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Retrieve the states of the sprites saved at the end of the previous run.
        Only the x,y,direction can be saved.
        The `identifier` is used to identifier which sprite is which. 

        To save the states of the sprites, refer to [`save_sprite_states`](./game_module#Game.save_sprite_states)

        Returns True if the states are loaded and False if not.

        Example:
        ```python
        my_sprite = pysc.create_circle_sprite((255,255,255), 5)

        def on_game_start():
            my_sprite.retrieve_saved_state()

        my_sprite.when_game_start().add_handler(on_game_start)
        ``` 
        """

        result = game._get_saved_state(self.identifier)
        if result:
            self.x = result['x']
            self.y = result['y']
            self.direction = result['direction']
            return True
        
        if not_exist_ok:
            return False
        
        raise KeyError(f"No saved stated found for this sprite: {self.identifier}")
    
    def lock_to(self, sprite: Sprite, offset: Tuple[float, float], reset_xy = False):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Locks in the position of this sprite relative to the position of another sprite, 
        so the sprite will always be in the same location relative to the other sprite.  
        This method only need to run once (instead of continuously in a loop)

        KNOWN ISSUE: Dragging a locked sprite will cause the sprite to go unpredictably. (It's unlikely that you would need to do that anyway.)

        Example: 
        ```python
        # a very rudimentary text bubble
        text_bubble_sprite = create_rect_sprite(...)

        # lock the position of the text_bubble_sprite relative to the player_sprite. 
        text_bubble_sprite.lock_to(player_sprite, offset=(-100, -100))

        # a very rudimentary implementation that assumes 
        # that you won't have more than one text message within 3 seconds
        def on_message(data):
        
            text_bubble_sprite.write_text(data)
            text_bubble_sprite.show()

            yield 3 # wait for three seconds
            text_bubble_sprite.hide()

        text_bubble_sprite.when_received_message('dialogue').add_handler(on_message)

        ```
        """
        assert self._body.body_type == pymunk.Body.KINEMATIC, "only KINEMATIC object can be locked to another sprite"
        
        self._lock_to_sprite = sprite
        self._lock_offset = offset
        if reset_xy: 
            self.x = 0
            self.y = 0

    def release_position_lock(self):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Release the position lock set by `lock_to`
        """        
        self._lock_to_sprite = None
        self._lock_offset = None
        pass

    # END: motions  


    # START: drawing related
    def set_rotation_style_all_around(self):
        """
        Same as the block "set rotation style [all around]" in Scratch. 
        Allow the image to rotate all around with `direction`
        """
        self._drawing_manager.set_rotation_style(_RotationStyle.ALL_AROUND)
        self.__rotation_style = _RotationStyle.ALL_AROUND

    def set_rotation_style_left_right(self):
        """
        Same as the block "set rotation style [left-right]" in Scratch. 
        Only allows the image to flip left or right depending on the `direction`. 

        Does not constrain the direction of movement to only left and right. 
        """        
        self._drawing_manager.set_rotation_style(_RotationStyle.LEFTRIGHT)
        self.__rotation_style = _RotationStyle.LEFTRIGHT

    def set_rotation_style_no_rotation(self):
        """
        Same as the block "set rotation style [don't rotate]" in Scratch. 
        Does not allow the image flip or rotate with `direction`. 

        Does not constrain the direction of movement.

        """
        self._drawing_manager.set_rotation_style(_RotationStyle.FIXED)
        self.__rotation_style = _RotationStyle.FIXED


    def set_frame(self, idx:int):
        """
        Same as the block "switch costume to [costume]" in Scratch, 
        except that you are specifying the frame (i.e. the costume) by the index. 
        
        TODO: link to sprite creation 
        """
        self._drawing_manager.set_frame(idx)
    
    def next_frame(self):
        """
        Same as the block "next costume" in Scratch, 
        """
        self._drawing_manager.next_frame()

    def set_animation(self, name:str):
        """
        *EXTENDED FEATURE*

        Changes the set of frames that is used by `set_frame` and `next_frame`.
        This is mainly for sprites that have different animations for different actions. 

        TODO: update the link
        See the [guide](https://kwdchan.github.io/pyscratch/) for more details.
        """   
        self._drawing_manager.set_animation(name)
        
    @property
    def frame_idx(self):
        """
        In Scratch, this is the costume number. 
        
        To change costume, you will need to call `set_frame`. 
        """
        return self._drawing_manager.frame_idx
    
    @property
    def animation_name(self):
        """
        *EXTENDED FEATURE*

        The name of the set of frames that is currently used. 

        Set by `set_animation`
        """        
        return self._drawing_manager.animation_name

    def set_scale(self, factor: float):
        """
        Sets the size factor of the sprite.

        For example:
        - A factor of 1.0 means 100% of the *original* image size
        - A factor of 1.2 means 120%
        - A factor of 0.8 means 80%
        """
        if self._drawing_manager.set_scale(factor):
            self._physics_manager.request_shape_update()

    def scale_by(self, factor: float):
        """
        Changes the size of the sprite by a factor

        For example:
        - A factor of 1.2 is a 20% increase of the *current* size (not original size)
        - A factor of 0.8 makes the sprite 80% of the *current* size
        """
        self._drawing_manager.scale_by(factor)
        self._physics_manager.request_shape_update()

    @property
    def scale_factor(self):
        """
        The scale factor of the sprite size
        """
        return self._drawing_manager.scale_factor

    def flip_horizontal(self, to_flip:bool):
        """
        Whether or not to flip the image horizontally. 
        Does not affect the direction of movement.
        """        
        self._drawing_manager.flip_horizontal(to_flip)

    def flip_vertical(self, to_flip:bool):
        """
        Whether of not to flip the image vertically. 
        Does not affect the direction of movement.
        """ 
        self._drawing_manager.flip_vertical(to_flip)

    def set_brightness(self, factor):
        """
        *EXPERIMENTAL*

        Changes the brightness of the sprite. 
        """ 
        self._drawing_manager.set_brightness(factor)

    def set_transparency(self, factor:float):
        """
        *EXPERIMENTAL*

        Changes the transparency of the sprite. 

        Parameters
        ---
        factor : float
            Transparency level from 0.0 (fully transparent) to 1.0 (fully opaque).
        """ 
        self._drawing_manager.set_transparency(factor)

    def write_text(self, text: str, font: pygame.font.Font, colour=(255,255,255), offset=(0,0), centre=True, reset=True):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Writes text on the sprite given a font. 
        ```python
        # if the font is shared by multiple sprites, consider putting it in `settings.py`
        font = pygame.font.SysFont(None, 48)  # None = default font, 48 = font size

        my_sprite.write_text("hello_world", font)

        ```
        Parameters
        ---
        text: str
            The text to display.

        font: pygame.font.Font
            The pygame font object. Refer to the website of pygame for more details. 
        
        colour: Tuple[int, int, int] or Tuple[int, int, int, int]
            The colour the of text. Takes RGB or RGBA, where A is the transparency. Value range: [0-255]

        offset: Tuple[float, float]
            The location of the text image relative to the sprite

        centre: bool
            If False, the top-left corner of the text, instead of the center, would be considered as its location.
        
        reset: bool
            Whether or not to clear all the existing drawing (including previous text)  

        """ 
        text_surface = font.render(text, True, colour) 
        self._drawing_manager.blit_persist(text_surface, offset, centre=centre, reset=reset)
    
    def draw(self, image: pygame.Surface,  offset=(0,0), centre=True, reset=True):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Draws an image on the sprite.
        ```python
        an_image = pysc.helper.load_image("assets/an_image.png")
        my_sprite.draw(an_image)
        ```
        Parameters
        ---
        image: pygame.Surface
            An image (pygame surface). You can use `helper.load_image` to load the image for you.

        offset: Tuple[float, float]
            The location of the image relative to the sprite

        centre: bool
            If False, the top-left corner of the image, instead of the center, would be considered as its location.
        
        reset: bool
            Whether or not to clear all the existing drawing (including the text)  

        """ 

        self._drawing_manager.blit_persist(image, offset, centre=centre, reset=reset)

    # END: drawing related    
    

    ## other blocks
    def is_touching(self, other_sprite) -> bool:
        """
        Returns whether or not this sprite is touching another sprite. 
        A hidden sprite cannot be touched for the consistency with Scratch. 

        This function detects whether there is any overlapping of the pixels of the two sprites that are not *fully transparent*

        Note that the detection is done on the original image before the effect of `set_transparency` is applied. 
        Therefore, the touching can still be detected even if you set the transparency to 1.0. 

        ```python
        if this_sprite.is_touching(another_sprite):
            print('hi')
        ```
        """
        
        # if not self in game._all_sprites_to_show: 
        #     return False
        
        # if not other_sprite in game._all_sprites_to_show:
        #     return False
        
        if not self._shown: 
            return False

        if not other_sprite._shown:
            return False
        
        if not pygame.sprite.collide_rect(self, other_sprite): 
            return False
        
        return not (pygame.sprite.collide_mask(self, other_sprite) is None)
    
    def is_touching_mouse(self):
        """
        Returns whether or not this sprite is touching the mouse
        """
        if not self._shown:
            return False
        
        mos_x, mos_y = pygame.mouse.get_pos()

        if not self.rect.collidepoint((mos_x, mos_y)): 
            return False

        x = mos_x-self.rect.left
        y = mos_y-self.rect.top
        
        return self.mask.get_at((x, y))
    
        

    # def is_touching(self, other_sprite) -> bool:
    #     """
    #     Returns whether or not this sprite is touching another sprite.
    #     """
    #     return pyscratch.game_module._is_touching(self, other_sprite)
    
    
    # def is_touching_mouse(self):
    #     """
    #     Returns whether or not this sprite is touching the mouse
    #     """
    #     return pyscratch.game_module._is_touching_mouse(self)
    
    def hide(self):
        """
        Hides the sprite. 
        The hidden sprite is still in the space but it cannot touch another sprites
        """
        game._hide_sprite(self)
        self._shown = False
        self._intend_to_show = False

    def show(self):
        """
        Shows the sprite.
        """        
        game._show_sprite(self)
        self._intend_to_show = True
        # self._shown is set to True only during the update 
        

    @override
    def remove(self, *_):
        """
        Removes the sprite and all the events and conditions associated to it. 
        Takes no parameter.

        Usage:
        ```python
        # remove the sprite.
        my_sprite.remove()
        ```
        """
        self.hide() # prevent collision
        game._remove_sprite(self) 
        self.__removed = True


    def create_clone(self):
        """
        *EXPERIMENTAL*

        Create a clone of this sprite. 
        Even though is method is provided to align with Scratch, 
        The prefered way to create identitical or similar sprites 
        is to create the sprite within a function or an event. 

        ***INCOMPLETE IMPLEMENTATION***: 
        - Transparency and brightness aren't transferred to the clone
        """

        sprite = type(self)(
            frame_dict = self._drawing_manager.frame_dict_original, 
            starting_mode = self._drawing_manager.animation_name, 
            position = (self.x, self.y),
            shape_type = self._physics_manager.shape_type, 
            shape_size_factor = self._physics_manager.shape_size_factor, 
            body_type = self._body.body_type, 
        )
        if not self._intend_to_show:
            sprite.hide()
        else: 
            sprite.show()

        if self.__rotation_style == _RotationStyle.LEFTRIGHT:
            sprite.set_rotation_style_left_right()
        elif self.__rotation_style == _RotationStyle.FIXED:
            sprite.set_rotation_style_no_rotation()
            
        sprite.direction = self.direction
        sprite.scale_by(self._drawing_manager.scale_factor)
        sprite.set_frame(self._drawing_manager.frame_idx)
        sprite.set_draggable(self.draggable)
        sprite.elasticity = self.elasticity
        sprite.friction = self.friction



        if self._body.body_type == pymunk.Body.DYNAMIC: 
            sprite.mass = self.mass
            sprite.moment = self.moment

        sprite._drawing_manager.set_rotation_style(self._drawing_manager.rotation_style)


        game._clone_event_manager.on_clone(self, sprite)
        return sprite


    # alias of pygame method

    def when_game_start(self, other_associated_sprites: Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered when you call `game.start`. 
        The event handler does not take in any parameter.

        Also associates the event to the sprite so the event is removed when the sprite is removed. 

        Parameters
        ---
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. 
            Removal of any of these sprites leads to the removal of the event. 
        """
        

        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_game_start(associated_sprites)

    def when_any_key_pressed(self, other_associated_sprites: Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered when a key is pressed or released. 
        Also associates the event to the sprite so the event is removed when the sprite is removed. 
        
        The event handler have to take two parameters:
        - **key** (str): The key that is pressed. For example, 'w', 'd', 'left', 'right', 'space'. 
            Uses [pygame.key.key_code](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) under the hood. 
        
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a press or a release

        Parameters
        ---
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
    
        """    
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_any_key_pressed(associated_sprites)

    def when_key_pressed(self, key, other_associated_sprites: Iterable[Sprite]=[]):
        """   
        Returns an `Event` that is triggered when a specific key is pressed or released. 
        Also associates the event to the sprite so the event is removed when the sprite is removed. 

        The event handler have to take one parameter:
        - **updown** (str): Either 'up' or 'down' that indicates whether it is a press or a release
        
        Parameters
        ---
        key: str
            The key that triggers the event. For example, 'w', 'd', 'left', 'right', 'space'. 
            Uses [pygame.key.key_code](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) under the hood. 

        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
             
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_key_pressed(key, associated_sprites)
    

    
    def when_this_sprite_clicked(self, other_associated_sprites: Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered when the given sprite is clicked by mouse. 
        Also associates the event to the sprite so the event is removed when the sprite is removed. 

        The event handler does not take in any parameter.
                
        Parameters
        ---
        sprite: Sprite
            The sprite on which you want the click to be detected. The removal of this sprite will lead to the removal of this event so
            it does not need to be included in `other_assoicated_sprite`
        
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """        
        return game.when_this_sprite_clicked(self, other_associated_sprites)
       
    def when_backdrop_switched(self, idx, other_associated_sprites : Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered when the game is switched to a backdrop at `backdrop_index`.
        Also associates the event to the sprite so the event is removed when the sprite is removed. 
        
        The event handler does not take in any parameter.

        Parameters
        ---
        backdrop_index: int
            The index of the backdrop  

        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_backdrop_switched(idx, associated_sprites)
    
    def when_any_backdrop_switched(self, other_associated_sprites : Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered when the backdrop is switched. 
        Also associates the event to the sprite so the event is removed when the sprite is removed. 
        
        The event handler have to take one parameter:
        - **idx** (int): The index of the new backdrop  
        
        Parameters
        ---
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """        
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_any_backdrop_switched(associated_sprites)

    def when_timer_above(self, t, other_associated_sprites : Iterable[Sprite]=[]):
        """      
        Returns a `Condition` that is triggered after the game have started for `t` seconds.
        A `Condition` works the same way an `Event` does. 

        Also associates the condition to the sprite so the condition is removed when the sprite is removed. 


        The event handler have to take one parameter:
        - **n** (int): This value will always be zero

        Parameters
        ---
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """        
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_timer_above(t, associated_sprites)
    
    def when_started_as_clone(self, associated_sprites: Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered after the given sprite is cloned by `Sprite.create_clone`.
        Cloning of the clone will also trigger the event. Thus the removal of original sprite does not remove the event. 

        The event handler have to take one parameter:
        - **clone_sprite** (Sprite): The newly created clone.
                
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
                
        return game.when_started_as_clone(self, associated_sprites)    

    def when_receive_message(self, topic: str, other_associated_sprites : Iterable[Sprite]=[]):
        """
        Returns an `Event` that is triggered after a message of the given `topic` is broadcasted.
        Also associates the event to the sprite so the event is removed when the sprite is removed. 
        
        The event handler have to take one parameter:
        - **data** (Any): This parameter can be anything passed on by the message.

        Parameters
        ---
        topic: str
            Can be any string. If the topic equals the topic of a broadcast, the event will be triggered. 
        other_associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        
        
        associated_sprites = list(other_associated_sprites) + [self]
        return game.when_receive_message(topic, associated_sprites)
    
    def broadcast_message(self, topic: str, data: Any=None):
        """
        Completely the same as `game.broadcast_message`. 
        Just an alias. 

        Sends a message of a given `topic` and `data`.
        Triggers any event that subscribes to the topic. 
        The handlers of the events will receive `data` as the parameter.

        Example:
        ```python
        def event_handler(data):
            print(data) # data will be "hello world!"

        my_sprite.when_receive_message('print_message').add_handler(event_handler)
        my_sprite2.broadcast_message('print_message', data='hello world!')

        # "hello world!" will be printed out
        ```
        Parameters
        ---
        topic: str
            Can be any string. If the topic of an message event equals the topic of the broadcast, the event will be triggered. 

        data: Any
            Any arbitory data that will be passed to the event handler
        
        """
        return game.broadcast_message(topic, data)


    ## additional events
    def when_condition_met(self, checker=lambda: False, repeats: Optional[int]=None, other_associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE*

        For every frame, if a condition is met, the event is triggered. Repeated up to `repeats` times. 

        The condition is provided by a function that takes no argument and returns a boolean. 
        
        ```python
        def slowly_move_sprite_out_of_edge(n):
            my_sprite.x += 1
            
        my_sprite.when_condition_met(lambda: (my_sprite.x<0), None).add_handler(slowly_move_sprite_out_of_edge)
        ```

        The event handler have to take one parameter:
        - **n** (int): The number of remaining repeats

        Parameters
        ---
        checker: Callable[[], bool] 
            A function that takes no argument and returns a boolean. 
            The checker is run one every frame. If it returns true, the handler is called. 

        repeats: int or None
            How many times to repeat. Set to None for infinite repeats. 

                    
        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """

        associated_sprites = list(other_associated_sprites) + [self]

        return game.when_condition_met(checker, repeats, associated_sprites)
    
    
    def when_timer_reset(self, reset_period: Optional[float]=None, repeats: Optional[int]=None, other_associated_sprites: Iterable[Sprite]=[]):
        """
        *EXTENDED FEATURE, EXPERIMENTAL*

        Returns a `Condition` that is triggered after the game have started for `t` seconds.
        A `Condition` works the same way an `Event` does. 

        The event handler have to take one parameter:
        - **n** (int): This value will always be zero

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        associated_sprites = list(other_associated_sprites) + [self]

        return game.when_timer_reset(reset_period, repeats, associated_sprites)
    
    
    def start_handler(self, handler:Optional[Callable[[], Any]]=None,  other_associated_sprites : Iterable[Sprite]=[]):
        """
        Run the event handler immediately. Useful when creating a sprite within a function.

        The handler does not take in any parameters. 

        Parameters
        ---
        handler: Function
            A function to run. 

        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        
        """
        
        associated_sprites = list(other_associated_sprites) + [self]
        return game.start_handler(handler, associated_sprites)
    
    
    def create_specific_collision_trigger(self, other_sprite: Sprite, other_associated_sprites: Iterable[Sprite]=[]):
        """
        @private
        *EXTENDED FEATURE, EXPERIMENTAL*

        DOCUMENTATION NOT COMPLETED

        Parameters
        ---
        associated_sprites: List[Sprite]
            A list of sprites that this event depends on. Removal of any of these sprites leads to the removal of the event. 
        """
        return game._create_specific_collision_trigger(self, other_sprite, other_associated_sprites)
    

    # START: TODO: physics property getters and setters

    def set_shape(self, shape_type: ShapeType=ShapeType.BOX):
        """
        @private
        *EXTENDED FEATURE, EXPERIMENTAL*
        
        Sets the collision shape of the sprite. The shape type can be one of the followings
        - box
        - circle
        - circle_height
        - circle_width

        You can think of the collision shape as the actual shape of the sprite, 
        while the sprite image (the costume) is just like a phantom projection 
        that cannot be touched.

        To see what it means, set `debug_draw` to True when you start the game. 
        ```python
        game.start(60, debug_draw=True)
        ```
        """
        self._physics_manager.set_shape_type(shape_type)
    
    def set_shape_size_factor(self, factor=0.8):
        """
        @private

        *EXTENDED FEATURE, EXPERIMENTAL*

        Changes the size of the collision shape relative to the size of the image of the sprite. 
        For example: 
        - factor = 1.0 -> same size
        - factor = 0.8 -> the collision shape is 80% of the sprite image 
        - factor = 1.2 -> the collision shape is 120% of the sprite image
        
        """
        self._physics_manager.set_shape_size_factor(factor)
    
    def set_collision_type(self, value: int=0):
        """
        @private
        *EXTENDED FEATURE, EXPERIMENTAL*

        Set the collision type of the sprite for detection purposes.
        The collision type can be any integer except that 
        **a sprite with a collision type of 0 (which is the default) will not collide with anything.**

        Note that touching can still be detected.
        """
        self._physics_manager.set_collision_type(value)

    @property
    def mass(self):
        """
        @private
        *EXTENDED FEATURE*

        The mass of the collision shape. 
        Only work for dynamic objects.

        You can make changes to this property. 
        """
        return self._body.mass
    
    @property
    def moment(self):
        """
        @private
        *EXTENDED FEATURE*

        The moment of the collision shape. 
        The lower it is, the more easy it spins. 
        Only work for dynamic objects.

        You can make changes to this property. 
        """
        return self._body.moment
    
    @property
    def elasticity(self):
        """
        @private
        *EXTENDED FEATURE*

        The elasticity of the collision shape. 
        Elasticity of 1 means no energy loss after each collision. 

        You can make changes to this property. 
        """
        return self._shape.elasticity
    
    @property
    def friction(self):
        """
        @private
        *EXTENDED FEATURE*

        The friction of the collision shape. 

        You can make changes to this property. 
        """
        return self._shape.friction
    
    @mass.setter
    def mass(self, value):
        self._body.mass = value

    @moment.setter
    def moment(self, value):
        self._body.moment = value
    
    @elasticity.setter
    def elasticity(self, value):
        self._physics_manager.elasticity = value
    
    @friction.setter
    def friction(self, value):
        self._physics_manager.friction = value
    
    # END: physics property



def __create_edges_for_on_edge_bounce():
    t, l, b, r = create_edge_sprites((255, 255, 255, 255), thickness=0, collision_type=0)

    t.identifier = "default_edge_t"
    l.identifier = "default_edge_l"
    b.identifier = "default_edge_b"
    r.identifier = "default_edge_r"

    game._top_edge = t
    game._left_edge = l
    game._bottom_edge = b
    game._right_edge = r

game.when_game_start().add_handler(__create_edges_for_on_edge_bounce)