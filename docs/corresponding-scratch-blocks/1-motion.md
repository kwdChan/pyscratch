---
title: Motion
parent: Corresponding Scratch Blocks
nav_order: 1
---

# Motion

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_00.png" height="10"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.move_indir">
    <code>my_sprite.move_indir(10)</code>
    </a>
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_01.png" height="10"/>
  </div>
  <div class="col">
    <code>my_sprite.direction += 15</code>
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_02.png" height="10"/>
  </div>
  <div class="col">
    <code>my_sprite.direction -= 15</code>
  </div>
</div>


<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_04.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.x = 0</code>
        <code>my_sprite.y = 0</code>
        OR
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.set_xy"><code>my_sprite.set_xy((0,0))</code></a>
        
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_03.png" height="10"/>
  </div>
  <div class="col">
        <a target="_blank" href="../pdoc/pyscratch/helper.html#random_number">
            <code>x = pysc.random_number(0, 100)</code>
        </a>
        <code>y = pysc.random_number(0, 100)</code>
        <code>my_sprite.set_xy((x,y))</code>
        <br>
        OR
        <br>
        <br>
        <a target="_blank" href="../pdoc/pyscratch/game_module.html#get_mouse_pos">
            <code>x, y = pysc.get_mouse_pos()</code>
        </a>
        <code>my_sprite.set_xy((x,y))</code>
        <br>
        OR
        <br>
        <br>
        <code>x = another_sprite.x</code>
        <code>y = another_sprite.y</code>
        <code>my_sprite.set_xy((x,y))</code>

  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_05.png" height="10"/>
  </div>
  <div class="col">
        NOT YET IMPLEMENTED
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_06.png" height="10"/>
  </div>
  <div class="col">
        NOT YET IMPLEMENTED
  </div>
</div>


<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_07.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.direction = 90</code>
  </div>
</div>



<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_08.png" height="10"/>
  </div>
  <div class="col">
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.point_towards_sprite">
            <code>my_sprite.point_towards_sprite(another_sprite)</code>
        </a>
        OR
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.point_towards_mouse">
            <code>my_sprite.point_towards_mouse()</code>
        </a>
        OR
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.point_towards">
            <code>my_sprite.point_towards((100, 100))</code>
        </a>
  </div>
</div>



<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_09.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.x += 10</code>
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_10.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.x = 0</code>
  </div>
</div>


<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_11.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.y += 10</code>
  </div>
</div>

<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_12.png" height="10"/>
  </div>
  <div class="col">
        <code>my_sprite.y = 0</code>
  </div>
</div>


<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_13.png" height="10"/>
  </div>
  <div class="col">
        {%include new_tab_hyperlink.html
          url="../pdoc/pyscratch/sprite.html#Sprite.if_on_edge_bounce" 
          content="<code>my_sprite.if_on_edge_bounce()</code> (An approximation implementation)" 
        %}
  </div>
</div>



<div class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/motion/block_14.png" height="10"/>
  </div>
  <div class="col">
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.set_rotation_style_all_around">
            <code>my_sprite.set_rotation_style_all_around()</code>
        </a>
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.set_rotation_style_left_right">
            <code>my_sprite.set_rotation_style_left_right()</code>
        </a>
        <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.set_rotation_style_no_rotation">
            <code>my_sprite.set_rotation_style_no_rotation()</code>
        </a>

  </div>
</div>
