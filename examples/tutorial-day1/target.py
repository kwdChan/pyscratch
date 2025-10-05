import pyscratch as pysc
game = pysc.game
target = pysc.create_single_costume_sprite("assets/target_b.png")

# 3. Flow control
def follow_mouse():
    game.bring_to_front(target)
    while True:
        yield 1/game.framerate
        mouse_x, mouse_y = pysc.get_mouse_pos()
        target.x = mouse_x
        target.y = mouse_y
    
target.when_game_start().add_handler(follow_mouse)