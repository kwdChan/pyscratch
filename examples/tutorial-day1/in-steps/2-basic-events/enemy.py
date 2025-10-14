import pyscratch as pysc
game = pysc.game

enemy = pysc.create_single_costume_sprite("assets/fish_red_skeleton_outline.png")
#enemy.set_draggable(True)


def clicked():
    """
    when the enemy is clicked: 
    change the enemy location
    """

    enemy.x = pysc.random_number(0, game.screen_width)
    enemy.y = pysc.random_number(0, game.screen_height)
    

enemy.when_this_sprite_clicked().add_handler(clicked)
