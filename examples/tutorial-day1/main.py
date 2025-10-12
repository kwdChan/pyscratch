import pyscratch as pysc
import pygame
import target, enemy, chest, friend#, text

game = pysc.game

# mouse 
pygame.mouse.set_visible(False)


# background
bg0 = pysc.load_image("assets/undersea_bg.png")
bg0 = pysc.scale_to_fit_aspect(bg0, (1024, 576))
game.add_backdrop('bg0', bg0)

bg1 = pysc.load_image("assets/Cat In Space Wallpaper Hq.jpg")
bg1 = pysc.scale_to_fit_aspect(bg1, (1024, 576))
game.add_backdrop('bg1', bg1)

game.switch_backdrop('bg0')

# sound
game.load_sound("hit", "assets/impactMetal_light_004.ogg")
game.load_sound("background", "assets/Circus-Theme-Entry-of-the-Gladiators-Ragtime-Version(chosic.com).mp3")

def play_loop():
    while True:
        game.play_sound("background", volume=0)
        yield 2*60+33
game.when_game_start().add_handler(play_loop)




def background():
    while True:
        yield 1/game.framerate
        if game['score'] < 0: 
            game.switch_backdrop('bg1')

        
game.when_game_start().add_handler(background)


game.update_screen_mode((1024, 576))
game.start(show_mouse_position=True)


