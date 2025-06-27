---
title: Control
parent: Corresponding Scratch Blocks
nav_order: 5
---
# Control
<div id="wait" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/control/block_11.png"/>
  </div>
  <div class="col">
{% highlight python %}
    yield 1
{% endhighlight %}
  </div>
</div>


<div id="repeat" class="two-col">
  <div class="col">
    <img class="big" src="{{ site.cdn_url }}img/control/block_00.png"/>
  </div>
  <div class="col">
    <p> Repeat 10 times instantly (within one frame)<br>
{% highlight python %}
    for i in range(10): 
        # do something 
{% endhighlight %}
    </p>
    <p> Repeat 10 times over time
    <br>
{% highlight python %}
    for i in range(10): 
        # do something 
        yield 1/60 # wait for some time
{% endhighlight %}
    </p>
  </div>
</div>

<div id="forever" class="two-col">
  <div class="col">
    <img class="big" src="{{ site.cdn_url }}img/control/block_01.png"/>
  </div>
  <div class="col">
{% highlight python %}
    while True:
        # do something 
        yield 1/60
{% endhighlight %}
  </div>
</div>
<div id="if" class="two-col">
  <div class="col">
    <img class="big" src="{{ site.cdn_url }}img/control/block_02.png"/>
  </div>
  <div class="col">
{% highlight python %}
    if condition: 
        # do something
{% endhighlight %}
  </div>
</div>

<div id="if_else" class="two-col">
  <div class="col">
    <img class="big" style="max-height: 130px;" src="{{ site.cdn_url }}img/control/block_03.png"/>
  </div>
  <div class="col">
{% highlight python %}
    if condition: 
        # do something
    else: 
        # do something else
{% endhighlight %}
  </div>
</div>


<div id="wait_for_condition" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/control/block_04.png"/>
  </div>
  <div class="col">
{% highlight python %}
    while not condition: 
        yield 1/60 
    # after the condition is met
{% endhighlight %}
  </div>
</div>

<div id="repeat_until" class="two-col">
  <div class="col">
    <img class="big" src="{{ site.cdn_url }}img/control/block_05.png"/>
  </div>
  <div class="col">
{% highlight python %}
    while condition: 
        # do something 
        yield 1/60 
{% endhighlight %}
  </div>
</div>

<div id="stop_all" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/control/block_06.png"/>
  </div>
  <div class="col">
    Remove specific sprites:<br>
    <a target="_blank" href="../../pdoc/pyscratch/sprite.html#Sprite.remove">
    <code>my_sprite.remove()</code>
    </a> 
    <br>
    <a target="_blank" href="../../pdoc/pyscratch/event.html#Event.remove">Remove specific events:</a><br>
    {% highlight python %}
    my_event = my_sprite.when_game_start()
    my_event.add_handler(my_handler)

    # later on when the event is no longer needed 
    my_event.remove()
    {% endhighlight %}
   </div>
</div>


<div id="when_started_as_clone" class="two-col">
  <div class="col">
    <img class="bigger" src="{{ site.cdn_url }}img/control/block_07.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../../pdoc/pyscratch/sprite.html#Sprite.when_started_as_clone">
    <code>my_sprite.when_started_as_clone()</code>
    </a>
  </div>
</div>



<div id="create_clone" class="two-col">
  <div class="col">
    <img  src="{{ site.cdn_url }}img/control/block_08.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../../pdoc/pyscratch/sprite.html#Sprite.create_clone">
    <code>my_sprite.create_clone()</code>
    </a>  
</div>
</div>



<div id="delete_clone" class="two-col">
  <div class="col">
    <img src="{{ site.cdn_url }}img/control/block_09.png"/>
  </div>
  <div class="col">
    <a target="_blank" href="../../pdoc/pyscratch/sprite.html#Sprite.remove">
    <code>clone_sprite.remove()</code>
    </a>     
  </div>
</div>
