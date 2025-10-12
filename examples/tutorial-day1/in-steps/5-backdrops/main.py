import pyscratch as pysc
import chest, enemy, friend
game = pysc.game

       
# background
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576))

bg1 = pysc.load_image("assets/Cat In Space Wallpaper Hq.jpg")
bg1 = pysc.scale_to_fit_aspect(bg1, (1024, 576))

game.set_backdrops([bg0, bg1])

game.switch_backdrop(0)



# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)


