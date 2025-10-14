import pyscratch as pysc
from pyscratch import game

chest = pysc.create_single_costume_sprite("assets/chest-open.png")

# 1. Create a function that does the thing (any function name is fine)
def set_size_position(): 
    """
    when game start:
    set the initial position of the chest
    """
    chest.set_scale(0.5)
    chest.x = game.screen_width/2
    chest.y = game.screen_height/2
    game.move_to_back(chest)

# 2. Create an event object (any event name is fine)
#click_event = chest.when_this_sprite_clicked() 

# 3. Attach the function to the event block
#click_event.add_handler(set_size_position) 

# Or step 2 and 3 together in one line
#chest.when_this_sprite_clicked().add_handler(set_size_position)
chest.when_game_start().add_handler(set_size_position)