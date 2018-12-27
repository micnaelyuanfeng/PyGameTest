import pygame
from macroDefines import *

class interrupt_handler(object):
    def __init__(self):
        pass
    
    def keyboard_event(self, event):
        key_direction = KEY_DIRECTION_INVALID
        key_space     = 0
        key_fire      = None

        key_list      = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                key_direction = KEY_DIRECTION_RIGHT
            elif event.key == pygame.K_LEFT:
                key_direction = KEY_DIRECTION_LEFT
            elif event.key == pygame.K_UP:
                key_direction = KEY_DIRECTION_UP
            elif event.key == pygame.K_DOWN:
                key_direction = KEY_DIRECTION_DOWN
            elif event.key == pygame.K_SPACE:
                key_space = MARIO_JUMP
            elif event.key == pygame.K_x:
                key_fire = FIRE_ENABLE

        key_list.append(key_direction)
        key_list.append(key_space)
        key_list.append(key_fire)

        return key_list
    
    def mouse_position_event(self, event):
        mouse_position_x = MOUSE_POSITION_INVALID
        mouse_position_y = MOUSE_POSITION_INVALID

        if event.type == pygame.MOUSEMOTION:
            mouse_position_x, mouse_position_y = event.pos
        
        return mouse_position_x, mouse_position_y

    def mouse_button_event(self, event):
        mouse_button_left  = MOUSE_BUTTON_INVALID
        mouse_button_right = MOUSE_BUTTON_INVALID
        mouse_left_up      = MOUSE_BUTTON_INVALID
        mouse_left_down    = MOUSE_BUTTON_INVALID
        mouse_right_up     = MOUSE_BUTTON_INVALID
        mouse_right_down   = MOUSE_BUTTON_INVALID

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                mouse_button_left = MOUSE_BUTTON_LEFT
                mouse_left_down   = MOUSE_BUTTON_LEFT_DOWN
            elif event.button == RIGHT:
                mouse_button_right = MOUSE_BUTTON_RIGHT
                mouse_right_down   = MOUSE_BUTTON_RIGHT_DOWN
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT:
                mouse_button_left = MOUSE_BUTTON_LEFT
                mouse_left_up     = MOUSE_BUTTON_LEFT_UP
            elif event.button == RIGHT:
                mouse_button_right = MOUSE_BUTTON_RIGHT
                mouse_right_up     = MOUSE_BUTTON_RIGHT_UP

        return mouse_button_left, mouse_button_right, mouse_left_up, mouse_right_up, mouse_left_down, mouse_right_down
    
    def peripheral_event_handler(self, event):

        peripheral_list = {}

        peripheral_list[KEY_ACTION]         = self.keyboard_event(event)
        peripheral_list[MOUSE_MOVE_ACTION]  = self.mouse_position_event(event)
        peripheral_list[MOUSE_CLICK_ACTION] = self.mouse_button_event(event)

        return peripheral_list