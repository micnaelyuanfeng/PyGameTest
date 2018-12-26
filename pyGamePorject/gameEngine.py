import sys
import pygame
import os
import psutil

from gameElement import *

class game_engine(object):
    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        self.background_color = 0
        self.caption = ""

    def set_screen(self, width, height):
        self.screen_height = height
        self.screen_width  = width

        return pygame.display.set_mode(( self.screen_width, self.screen_height))
    
    def set_background_color(self, background_color):
        self.background_color = background_color
    
    def set_caption(self, caption):
        self.caption = caption
        pygame.display.set_caption(self.caption)

    def build_frame(self, screen, list):
        mario       = mario_block(screen)
        mario.set(screen, "marioBlock", True)
        
        background      = game_element(screen)
        background.set(screen, "background", False)

        questionBlock   = question_block(screen)
        questionBlock.set(screen, "questionBlock", True)

        goombaBlock1   = goomba_block(screen)
        goombaBlock1.set(screen, "goombaBlock", True)

        fireFlower     = fire_flower(screen)
        fireFlower.set(screen, "flowerBlock", True)

        list.append(background)
        list.append(mario)
        list.append(questionBlock)
        list.append(goombaBlock1)
        list.append(fireFlower)

        return list

    def update_screen(self, screen, element_list, peripheral_actions, frame_counter):
        for element in element_list:
            if element.element_name == "marioBlock":
                if frame_counter % 10 == 0:
                    if peripheral_actions[KEY_ACTION][KEY_DIRECTION_IDX] is not -1:
                        element.doing_jump = False
                        element.doing_running = True
                        element.doing_standing = False
                        if peripheral_actions[KEY_ACTION][KEY_DIRECTION_IDX] is KEY_DIRECTION_LEFT:
                            element.direction = KEY_DIRECTION_LEFT
                            if element.doing_jump is not True:
                                element.rect.centerx = element.rect.centerx - 1
                        elif peripheral_actions[KEY_ACTION][KEY_DIRECTION_IDX] is KEY_DIRECTION_RIGHT:
                            element.direction = KEY_DIRECTION_RIGHT
                            if element.doing_jump is not True:
                                element.rect.centerx = element.rect.centerx + 1
                        element.update_mario_frames(screen)
                    
                    elif element.jump_done == True and peripheral_actions[KEY_ACTION][KEY_SPACE_IDX] == MARIO_JUMP:
                        element.doing_running = False
                        element.doing_standing = False
                        element.doing_jump = True
                        element.jump_done = False
                        element.update_mario_frames(screen)
                    elif element.jump_done is True:
                        element.doing_jump = False
                        element.doing_running = False
                        element.doing_standing = True
                        element.update_mario_frames(screen)

                    if element.doing_jump is True:
                        if element.jump_direction == DIRECTION_UP:
                            element.rect.centery = element.rect.centery - 1
                        elif element.jump_direction == DIRECTION_DOWN:
                            element.rect.centery = element.rect.centery + 1
                        
                        if element.direction == KEY_DIRECTION_RIGHT:
                            element.rect.centerx = element.rect.centerx + 1
                        elif element.direction == KEY_DIRECTION_LEFT:
                            element.rect.centerx = element.rect.centerx - 1

                        if element.rect.centery == MATIO_POSITION_Y_INIT - MOVE_RANGE:
                            element.jump_direction = DIRECTION_DOWN
                        elif element.rect.centery == MATIO_POSITION_Y_INIT:
                            element.rect.centery = MATIO_POSITION_Y_INIT
                            element.jump_done = True
                            element.doing_jump = False
                            element.jump_direction = DIRECTION_UP
                        
                        element.update_mario_frames(screen)
                    else:
                        element.update_mario_frames(screen)

            if element.element_name == "goombaBlock":
                if frame_counter % 70 == 0:
                    if element.direction == DIRECTION_LEFT:
                        element.rect.centerx = element.rect.centerx - 1
                    elif element.direction == DIRECTION_RIGHT:
                        element.rect.centerx = element.rect.centerx + 1
            
                    if element.rect.centerx == GOOMBA_1_POSITION_X_INIT - MOVE_RANGE:
                        element.direction = DIRECTION_RIGHT
                    elif element.rect.centerx == GOOMBA_1_POSITION_X_INIT + MOVE_RANGE:
                        element.direction = DIRECTION_LEFT
    
    def respond_to_event(self):
        pass

    def get_screen_size(self):
        return self.screen_height, self.screen_width

    def draw_line(self, points, start, end, width, color):
        pass

    def display_sys_info(self):
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUsage = py.memory_info()[0]/2.**30