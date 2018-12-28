import sys
import pygame
import os

from interrupt    import *
from gameElement  import *
from gameEngine   import *
from macroDefines import *

game_list = {}
bg_color = (230, 230, 230)

if __name__ == "__main__":
    keyboardHanlder = interrupt_handler()
    gameEngine      = game_engine()
    pygame.init()
    
    screen = gameEngine.set_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.fill(bg_color)
    
    gameEngine.set_caption("Mario Custom Game" )
    gameEngine.build_frame(screen, game_list)

    frame_counter = 0

    key_direction = -1
  
    while True:
        key_direction = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                peripheral_actions = keyboardHanlder.peripheral_event_handler(event)
        gameEngine.check_mashroom_and_flower(game_list)
        gameEngine.check_mario_eat(game_list)
        gameEngine.check_fire(screen, peripheral_actions[KEY_ACTION], game_list)
        gameEngine.check_goomba_alive(game_list)
        gameEngine.check_fireball(game_list)

        if game_list[KEY_MARIO].eat_done is True:
            gameEngine.update_screen(screen, game_list, peripheral_actions, frame_counter)
        elif game_list[KEY_MARIO].eat_done is False:
            gameEngine.update_mario_grow_screen(screen, game_list[KEY_MARIO])

        for key, element in game_list.items():
            element.draw(screen, element.get_element_name(), frame_counter)

        if frame_counter == 10000000:
            frame_counter = 0
        else:
            frame_counter = frame_counter + 1

        pygame.display.flip()
