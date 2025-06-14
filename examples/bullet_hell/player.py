import pyscratch as pysc
from setting import *


def spawn_player(event_test=False):

   ...pyscratch# main sgame   player = pysc.create_rect_sprite((0, 0, 255), 50, 30, pos=(720//2, 1200))
    #pysc.game.add_sprite(player)
    player.set_collision_type(PLAYER_TYPE)


    # custom data
    pysc.game.shared_data['player'] = player
    pysc.game.shared_data['player_health'] = 10
    pysc.game.shared_data['bullet_period_ms'] = 200

    # behaviour
    ## 1. move by key press in a limited area
    ## 2. health changes on message
    ## 3. shoot bullet every n seconds (by messages)

    ## 1. movement    
    movement_event = pysc.game.when_timer_reset(1000/120)
    def movement(_):
        if game.is_key_pressed('w'):
            player.move_xy((0, -5))

        if game.is_key_pressed('s'):
            player.move_xy((0, 5))

        if game.is_key_pressed('a'):
            player.move_xy((-5, 0))

        if game.is_key_pressed('d'):
            player.move_xy((5, 0))

        player.set_xy((cap(player.x, 50, SCREEN_WIDTH-50), cap(player.y, SCREEN_HEIGHT-900, SCREEN_HEIGHT)))
    
    movement_event.add_handler(movement)


    ## 2. health changes on message
    health_change_event = pysc.game.when_receive_message('player_health')

    def health_change(change):
        pysc.game.shared_data['player_health'] += change

    health_change_event.add_handler(health_change)


    ## 3. bullets 
    bullet_timer = pysc.Timer()
    condition = lambda: (bullet_timer.read() > pysc.game.shared_data['bullet_period_ms'])
    shoot_bullet_event = pysc.game.when_condition_met(condition)

    def shoot_bullet(n):
        pysc.game.broadcast_message('player_shoot_bullet', player)
        bullet_timer.full_reset()

    shoot_bullet_event.add_handler(shoot_bullet)

    

    # health bar
    healthbar_empty = pysc.create_rect_sprite((255, 255, 255), 60, 5, pos=(0,0))
    #pysc.game.add_sprite(healthbar_empty)
    healthbar_empty.lock_to(player, (0,-30))

    ## move the health bar
    healthbar_red = pysc.create_rect((255, 0, 0), 60, 50)
    healthbar_empty.blit(healthbar_red, (0,0))

    # reusing the health_change_event defined about
    def on_health_change(change):
        new_health = max(0, pysc.game.shared_data['player_health'])

        healthbar_red = pysc.create_rect((255, 0, 0), 60*(new_health/10), 50)
        healthbar_empty.blit(healthbar_red)
    
    health_change_event.add_handler(on_health_change)

    if event_test: 
        shoot_bullet_event.remove()




spawn_player(event_test=False)

