import pyscratch as pysc
from pyscratch import game

msg = pysc.create_single_costume_sprite("assets/youlose.png")

def gamestart():
    """scale and hide on game start"""
    msg.scale_by(10)
    msg.hide()
    msg.x = 150
    msg.y = 150

msg.when_game_start().add_handler(gamestart)


def show_msg():
    """
    show message when lose
    """
    msg.show()

msg.when_backdrop_switched("lose").add_handler(show_msg)