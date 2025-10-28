import pyscratch as pysc
from pyscratch import game

chest = pysc.create_single_costume_sprite("assets/chest-open.png")

@chest.when_this_sprite_clicked()
def my_click_event():
    message = "I am a chest! "
    n_repeat = 4
    repeated_message = message * n_repeat
    print(repeated_message)
