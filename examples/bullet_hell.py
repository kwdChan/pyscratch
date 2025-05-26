import pymunk
from pyscratch import sensing
from pyscratch.scratch_sprite import ScratchSprite, create_rect, rect_sprite
from pyscratch.helper import get_frame_dict
from pyscratch.game import Game
import pygame

game = Game((720, 1280))
sprite_sheet = pygame.image.load("assets/09493140a07b68502ef63ff423a6da3954d36fd8/Green Effect and Bullet 16x16.png").convert_alpha()

font = pygame.font.SysFont(None, 24)  # None = default font, 48 = font size


frames = get_frame_dict(sprite_sheet, 36, 13, {
    "spin": [i+4*36 for i in range(14, 17+1)], 
    "star_explosion": [i+4*36 for i in range(19, 22+1)], 
    "heal": [i+1*36 for i in range(24, 28+1)], 
    "circle_explosion": [i+5*36 for i in range(14, 17+1)], 


    "square_bullets": [i+9*36 for i in range(24, 28+1)]+[i+9*36 for i in range(27, 24, -1)], 
    "circle_bullets": [i+8*36 for i in range(24, 28+1)]+[i+8*36 for i in range(27, 24, -1)], 

    "shield": [i+5*36 for i in [17]], 

    "bullet1": [i+3*36 for i in range(7, 7+1)]
})



start_buttom = rect_sprite((200, 0, 0), width=150, height=60, pos=(game.screen.get_width()//2, game.screen.get_height()//2))
start_buttom.write_text("Click to Start", font)
game.add_sprite(start_buttom)

def on_click():
    start_buttom.scale_by(0.9)

    on_condition = game.create_conditional_trigger(
        lambda: (not sensing.get_mouse_presses()[0]), repeats=1)
    
    def start_game(x):
        start_buttom.scale_by(1/0.9)
        game.boardcast_message('game_start', {'count': 0})
        game.remove_sprite(start_buttom)

    on_condition.add_callback(start_game)

#game.retrieve_sprite_click_trigger(start_buttom).add_callback(on_click)
on_click()


game.suppress_type_collision(4, True)

def shoot_player_bullet(origin):

    bullet = ScratchSprite(frames, "circle_bullets", origin)

    game.add_sprite(bullet)
    bullet.set_collision_type(4)
    bullet.set_rotation(-90)
    #bullet.body.velocity = (0, -.3)
    game.create_timer_trigger(1000/240).on_reset(
        lambda x: bullet.move_indir(2)
    )
    game.create_timer_trigger(100).on_reset(
        lambda x: bullet.next_frame()
    )



    # TODO: destory the bullet and the event when going out of the screen 
    # TODO: check the variable type when taking in the callback?

    




def game_start(data):

    player = rect_sprite((0, 0, 255), 50, 30, pos=(720//2, 1200), body_type=pymunk.Body.DYNAMIC)
    game.add_sprite(player)
    game.create_edges()
    player.set_collision_type(2)
    #bullet = ScratchSprite(frames, "circle_bullets", (400, 400))

    #bullet.set_scale(4)

    #game.add_sprite(bullet)



    game.create_timer_trigger(200).on_reset(lambda x: shoot_player_bullet((player.x, player.y)))




    def run_forever(_):
        if sensing.is_key_pressed(['w']):
            player.move_xy((0, -5))

        if sensing.is_key_pressed(['s']):
            player.move_xy((0, 5))

        if sensing.is_key_pressed(['a']):
            player.move_xy((-5, 0))

        if sensing.is_key_pressed(['d']):
            player.move_xy((5, 0))

        

    game.create_timer_trigger(1000/120).on_reset(run_forever)

    #game.create_collision_trigger(game.shared_data['bottom_edge'], player).add_callback(lambda a: player.move_xy((0, -50)))
    #game.create_collision_trigger(game.shared_data['bottom_edge'], player).add_callback(lambda a: print(a.shapes[1].collision_type))
    #game.create_collision_trigger(game.shared_data['bottom_edge'], player).add_callback(lambda a: print(a.shapes[0].collision_type))

    # about the collision suppression: 
    # two the earlier overwrite the later
    # call order: type2type -> default ->  type wildcard (not implemented)
    #game.create_type2type_collision_trigger(4, 2, True).add_callback(lambda a: print(2))
    #game.create_type_collision_trigger(2, True).add_callback(lambda a: print(1))


wait_for_game_start = game.create_messager_trigger('game_start').add_callback(game_start)


game.start(60, 300, False)