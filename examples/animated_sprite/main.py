import pyscratch as pysc
import my_sprite


pysc.create_edge_sprites(thickness=0)
pysc.game.update_screen_mode((1280, 720))
pysc.game.start()