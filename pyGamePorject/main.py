import sys
import pygame

from interrupt import *

def run_session(keyboardHanlder):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Test Game")

    bg_color = (230, 230, 230)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            x,y,z = keyboardHanlder.peripheral_event_handler(event)

            screen.fill(bg_color)
            pygame.display.flip()

if __name__ == "__main__":
    keyboardHanlder = interrupt_handler()
    run_session(keyboardHanlder)