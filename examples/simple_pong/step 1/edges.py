import pyscratch as pysc
game = pysc.game 

top_edge, left_edge, bottom_edge, right_edge = pysc.create_edge_sprites()

game['top_edge'] = top_edge
game['left_edge'] = left_edge
game['bottom_edge'] = bottom_edge
game['right_edge'] = right_edge
