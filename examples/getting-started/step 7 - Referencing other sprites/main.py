from numpy import deg2rad
import pyscratch as pysc
import player, enemy, hearts

# backdrop
backdrop_img = pysc.load_image('assets/my_background.jpg') # load the image(s)
pysc.game.set_backdrops([backdrop_img]) # a list of all the backdrop images 
pysc.game.switch_backdrop(0) # use the backdrop at index 0 


# start the game
screen_height = 720
screen_width = 1280
framerate = 60

# add these to as shared variables so other sprites might use it
pysc.game['screen_height'] = screen_height
pysc.game['screen_width'] = screen_width
pysc.game['framerate'] = framerate

pysc.game.update_screen_mode((screen_width, screen_height))
pysc.game.start(framerate)

