import pyscratch as pysc
from pyscratch import game
#pysc.create_shared_data_display_sprite("speed_multiplier")

perk = pysc.create_single_costume_sprite("assets/tool_bomb.png")

def when_perk_clicked():
    """
    reduce speed multiplier when perk clicked
    """
    perk.hide()
    perk.x = pysc.random_number(0, game.screen_width/2)
    perk.y = pysc.random_number(0, game.screen_height/2)
    game['speed_multiplier'] *= 0.9

perk.when_this_sprite_clicked().add_handler(when_perk_clicked)




def game_start():
    """
    perk appears
    """
    while True:
        yield pysc.random_number(1, 3)
        perk.show()

perk.when_game_start().add_handler(game_start)


