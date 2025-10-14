import pyscratch as pysc
from pyscratch import game
import chest, enemy, friend

# sound
game.load_sound("hit", "assets/impactMetal_light_004.ogg")
game.load_sound("background", "assets/Circus-Theme-Entry-of-the-Gladiators-Ragtime-Version(chosic.com).mp3")

def play_loop():
    """
    Continuously play the background music 
    """
    while True:
        game.play_sound("background", volume=0.1)
        yield 2*60+31 + 2 # or you can just put 153 
game.when_game_start().add_handler(play_loop)

# background
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576))
game.add_backdrop('sea', bg0)

bg1 = pysc.load_image("assets/Cat In Space Wallpaper Hq.jpg")
bg1 = pysc.scale_to_fit_aspect(bg1, (1024, 576))
game.add_backdrop('lose', bg1)

# Background switches
game.switch_backdrop('sea')

def background():
    while True:
        yield 1/game.framerate
        if game['score'] < 0: 
            game.switch_backdrop('lose')
game.when_game_start().add_handler(background)


# starting the game
game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)


