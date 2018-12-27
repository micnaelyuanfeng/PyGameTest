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

        mashRoom       = mashroom(screen)
        mashRoom.set(screen, "mashroomBlock", False)

        fireBall       = fire_ball(screen)
        fireBall.set(screen, "fireballBlock", True)

        list[KEY_BACKGROUND] = background
        list[KEY_MARIO] = mario
        list[KEY_QUESTION] = questionBlock
        list[KEY_GOOMBA] = goombaBlock1
        list[KEY_FLOWER] = fireFlower
        list[KEY_MASHROOM] = mashRoom
        list[KEY_FIREBALL] = fireBall

        return list

    def update_screen(self, screen, element_list, peripheral_actions, frame_counter):
        for key, element in element_list.items():
            if element.element_name == "marioBlock":
                if frame_counter % 10 == 0:
                    if peripheral_actions[KEY_ACTION][KEY_DIRECTION_IDX] is not -1:
                        if element.jump_done == True:
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

                        if element.rect.centery == MARIO_POSITION_Y_INIT - MOVE_RANGE:
                            element.jump_direction = DIRECTION_DOWN
                        elif element.rect.centery == MARIO_POSITION_Y_INIT:
                            element.rect.centery = MARIO_POSITION_Y_INIT
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
    
    def check_mario_eat(self, element_list):
        mario = element_list[KEY_MARIO]
        mashroom = element_list[KEY_MASHROOM]
        flower   = element_list[KEY_FLOWER]

        if mario.rect.centerx == mashroom.rect.centerx and mario.rect.centery == mashroom.rect.centery:
            #print("Eat Mashroom")
            if mario.has_eat_something is False:
                mario.eat_mashroom = True
                mario.eat_done = False
        elif mario.rect.centerx == flower.rect.centerx and mario.rect.centery == flower.rect.centery:
            if mario.has_eat_something is False:
                mario.eat_flower = True
                mario.eat_done = False

    def get_screen_size(self):
        return self.screen_height, self.screen_width

    def update_mario_grow_screen(self, screen, mario):
        if mario.frame_counter < EAT_PERIOD_TIMESPAN:
            #print("called")
            if mario.eat_mashroom is True:
                if mario.flip_draw is False:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = True
                        mario.frame_step_counter = 0
                        current_pattern = "M*S*.png"
                        current_path = pathlib.Path('./small_mario_frames')
                        mario.update_mario_frames_grow(current_pattern, current_path)
                elif mario.flip_draw is True:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = False
                        mario.frame_step_counter = 0
                        current_pattern = "S*M*S*.png"
                        current_path = pathlib.Path('./big_mario_frames')
                        mario.update_mario_frames_grow(current_pattern, current_path)
                
                mario.frame_step_counter = mario.frame_step_counter + 1
            elif mario.eat_flower is True:
                pass
            else:
                pass

            mario.frame_counter = mario.frame_counter + 1
        else:
            print("grown done")
            mario.frame_counter = 0
            mario.eat_done = True
            mario.has_eat_something = True

    def display_sys_info(self):
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUsage = py.memory_info()[0]/2.**30