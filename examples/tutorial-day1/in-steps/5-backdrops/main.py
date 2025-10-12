import pyscratch as pysc
from pyscratch import game
import chest, enemy, friend
       
# background
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576))
game.add_backdrop('bg0', bg0)

bg1 = pysc.load_image("assets/Cat In Space Wallpaper Hq.jpg")
bg1 = pysc.scale_to_fit_aspect(bg1, (1024, 576))
game.add_backdrop('bg1', bg1)



def on_game_start():
    game.switch_backdrop('bg0')

game.when_game_start().add_handler(on_game_start)


# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)


