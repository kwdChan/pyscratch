---
title: Sensing
parent: Corresponding Scratch Blocks
nav_order: 6
---

# Sensing

<div id="touching" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_00.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.is_touching_mouse"><code>my_sprite.is_touching_mouse()</code></a> 
    <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.is_touching"><code>my_sprite.is_touching(another_sprite)</code></a> 
  </div>
</div>


<div id="touching_colour" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_01.png"/>
    <img src="{{ site.cdn_url }}img/sensing/block_02.png"/>
  </div>
  <div class="col">
    Will not implement
  </div>
</div>



<div id="distance_to" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_03.png"/>
  </div>
  <div class="col">
    <p> For the distance to mouse, use <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.distance_to"><code>my_sprite.distance_to</code></a> </p>
    {% highlight python %}
    mos_x, mos_y = pysc.get_mouse_pos()
    my_sprite.distance_to((mos_x, mos_y))
    {% endhighlight %}
    OR
    <br>
    <br>
    <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.distance_to_sprite"><code>my_sprite.distance_to_sprite(another_sprite)</code></a> 

  </div>
</div>




<div id="ask" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_04.png"/>
    <img src="{{ site.cdn_url }}img/sensing/block_05.png"/>
  </div>
  <div class="col">
    Not implemented yet

  </div>
</div>



<div id="key_press" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_06.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/game_module.html#is_key_pressed"><code>pysc.is_key_pressed("space")</code></a>   </div>
</div>



<div id="mouse_down" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_07.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/game_module.html#get_mouse_presses"><pre><code>left, middle, right = pysc.get_mouse_presses()</code></pre></a>   
    </div>
</div>


<div id="mouse_xy" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_08.png"/>
    <img src="{{ site.cdn_url }}img/sensing/block_09.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/game_module.html#get_mouse_pos"><pre><code>mouse_x, mouse_y = pysc.get_mouse_pos()</code></pre></a>   </div>
</div>


<div id="draggable" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_10.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/sprite.html#Sprite.set_draggable"><code>my_sprite.set_draggable(True) </code></a>   
    </div>
</div>



<div id="loudness" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_11.png"/>
  </div>
  <div class="col">
    Not Implemented
  </div>
</div>



<div id="timer" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_12.png"/>
    <img src="{{ site.cdn_url }}img/sensing/block_13.png"/>
  </div>
  <div class="col">
    {% highlight python %}
    # this timer cannot be reset
    time = pysc.game.read_timer()

    # custom timers
    my_timer = pysc.Timer()
    time = my_timer.read()
    my_timer.full_reset()
    {% endhighlight %}

  </div>

</div>

<div id="what_of_what" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_14.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../pdoc/pyscratch/game_module.html#Game.backdrop_index">
    <code>
    pysc.game.backdrop_index</code>
    </a>
  </div>

</div>


<div id="datetime" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_15.png"/>
    <img src="{{ site.cdn_url }}img/sensing/block_16.png"/>
  </div>
  <div class="col">
    <p>Try <a target="_blank" href="https://www.w3schools.com/python/python_datetime.asp">datetime</a></p>
  </div>

</div>

<div id="datetime" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/sensing/block_17.png"/>
  </div>
  <div class="col">
    Of course not implemented
  </div>

</div>
