import pyscratch as pysc
import player, hearts, enemy


# shared variable
pysc.game['screen_height'] = 720
pysc.game['screen_width'] = 1280
pysc.game['framerate'] = 60


# backdrop
backdrop_img = pysc.helper.load_image('assets/vecteezy/my_background.jpg')
pysc.game.set_backdrops([backdrop_img])
pysc.game.switch_backdrop(0)


# start the game
pysc.game.update_screen_mode((pysc.game['screen_width'], pysc.game['screen_height']))
pysc.game.start(pysc.game['framerate'])

