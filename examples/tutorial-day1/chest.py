import pyscratch as pysc
game = pysc.game

chest = pysc.create_single_costume_sprite("assets/chest-open.png")

# 2. Basic Event
def game_start(): 
    chest.set_scale(0.5)
    chest.x = game.screen_width/2
    chest.y = game.screen_height/2
    game.move_to_back(chest)


chest.when_game_start().add_handler(game_start)

# 6. Backdrop
def game_end(): 
    chest.hide()

chest.when_backdrop_switched(1).add_handler(game_end)

