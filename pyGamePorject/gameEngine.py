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

        list[KEY_BACKGROUND] = background
        list[KEY_MARIO] = mario
        list[KEY_QUESTION] = questionBlock
        list[KEY_GOOMBA] = goombaBlock1
        list[KEY_FLOWER] = fireFlower
        list[KEY_MASHROOM] = mashRoom
        #list[KEY_FIREBALL] = fireBall

        return list
    
    def check_fire(self, screen, key_acitions, element_list):
        if FIRE_ENABLE in key_acitions:
            if element_list[KEY_MARIO].eat_flower is True and element_list[KEY_MARIO].fire_fireball is False:              
                fireBall = fire_ball(screen)
                fireBall.set(screen, "fireballBlock", True)
                element_list[KEY_FIREBALL] = fireBall

                fireBall.rect.centerx = element_list[KEY_MARIO].rect.centerx + 7
                fireBall.rect.centery = element_list[KEY_MARIO].rect.centery + 2
                
                fireBall.bounce_direction = FIRE_BALL_BOUNCE_DOWN

                if element_list[KEY_MARIO].direction == KEY_DIRECTION_LEFT:
                    element_list[KEY_FIREBALL].direction = DIRECTION_LEFT
                else:
                    element_list[KEY_FIREBALL].direction = DIRECTION_RIGHT

                element_list[KEY_MARIO].fire_fireball = True

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
                                    if element.rect.centerx >= GROUND_BOUNDRY_X:
                                        element.rect.centerx = element.rect.centerx
                                    else:
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
                            if element.rect.centerx >= GROUND_BOUNDRY_X:
                                element.rect.centerx = element.rect.centerx
                            else:
                                element.rect.centerx = element.rect.centerx + 1
                        elif element.direction == KEY_DIRECTION_LEFT:
                            element.rect.centerx = element.rect.centerx - 1
                        
                        if element.eat_flower is True or element.eat_mashroom is True:
                            if element.rect.centery == BIG_MARIO_POSITION_Y - MOVE_RANGE:
                                element.jump_direction = DIRECTION_DOWN
                            elif element.rect.centery == BIG_MARIO_POSITION_Y:
                                element.rect.centery = BIG_MARIO_POSITION_Y
                                element.jump_done = True
                                element.doing_jump = False
                                element.jump_direction = DIRECTION_UP
                        else:
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
            
            if element.element_name == "fireballBlock":
                if frame_counter % 10 == 0:
                    if element.direction == DIRECTION_LEFT:
                        element.rect.centerx = element.rect.centerx - 1
                    elif element.direction == DIRECTION_RIGHT:
                        element.rect.centerx = element.rect.centerx + 1
            
                    if element.bounce_direction == FIRE_BALL_BOUNCE_DOWN:
                        element.rect.centery = element.rect.centery + 1 
                        if element.rect.centery == GROUND_BOUNDRY:
                            element.bounce_direction = FIRE_BALL_BOUNCE_UP
                    elif element.bounce_direction == FIRE_BALL_BOUNCE_UP:
                        element.rect.centery = element.rect.centery - 1
                        if element.rect.centery == GROUND_BOUNDRY - FIRE_BALL_JUMP_RANGE:
                            element.bounce_direction = FIRE_BALL_BOUNCE_DOWN
                    

    def check_fireball(self, element_list):
        if KEY_FIREBALL in element_list:
            if element_list[KEY_FIREBALL].rect.centerx < SCREEN_BOUNDRY_X_MIN or element_list[KEY_FIREBALL].rect.centerx > SCREEN_BOUNDRY_X_MAX:
                del element_list[KEY_FIREBALL]

                element_list[KEY_MARIO].fire_fireball = False

    def check_mario_eat(self, element_list):
        mario = element_list[KEY_MARIO]

        if mario.eat_mashroom is False:
            mashroom = element_list[KEY_MASHROOM]
            if mario.rect.centerx == mashroom.rect.centerx and mario.rect.centery == mashroom.rect.centery:
                if mario.has_eat_something is False:
                    mario.eat_mashroom = True
                    mario.eat_done = False

        if mario.eat_flower is False:      
            flower = element_list[KEY_FLOWER]
            if mario.eat_mashroom is True:
                if mario.rect.centery + BIG_MARIO_FLOWER_Y_GAP == flower.rect.centery and mario.rect.centerx == flower.rect.centerx:
                    mario.eat_flower = True
                    mario.eat_done = False
            else:
                if mario.rect.centery == flower.rect.centery and mario.rect.centerx == flower.rect.centerx:
                    if mario.has_eat_something is False:
                        mario.eat_flower = True
                        mario.eat_done = False

    def get_screen_size(self):
        return self.screen_height, self.screen_width

    def update_mario_grow_screen(self, screen, mario):
        draw_big = False
        if mario.frame_counter < EAT_PERIOD_TIMESPAN:
            if mario.eat_mashroom is True and mario.eat_flower is False:
                if mario.flip_draw is False:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = True
                        mario.frame_step_counter = 0
                        draw_big = False

                        mario.update_mario_frames_grow(screen, draw_big)
                elif mario.flip_draw is True:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = False
                        mario.frame_step_counter = 0
                        draw_big = True

                        mario.update_mario_frames_grow(screen, draw_big)
                
                mario.frame_step_counter = mario.frame_step_counter + 1
            
            elif mario.eat_flower is True:
                if mario.flip_draw is False:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = True
                        mario.frame_step_counter = 0
                        draw_big = False
                        mario.update_mario_frames_grow(screen, draw_big)
                elif mario.flip_draw is True:
                    if mario.frame_step_counter > EAT_PERIOD_STEP:
                        mario.flip_draw = False
                        mario.frame_step_counter = 0
                        draw_big = True
                        mario.update_mario_frames_grow(screen, draw_big)

                mario.frame_step_counter = mario.frame_step_counter + 1
            else:
                pass

            mario.frame_counter = mario.frame_counter + 1
        else:
            mario.frame_counter = 0
            mario.eat_done = True
            mario.has_eat_something = True

    def check_mashroom_and_flower(self, game_list):
        if game_list[KEY_MARIO].eat_mashroom is True:
            if KEY_MASHROOM in game_list: 
                del game_list[KEY_MASHROOM]
        if game_list[KEY_MARIO].eat_flower is True:
            if KEY_FLOWER in game_list:
                del game_list[KEY_FLOWER]
    
    def check_goomba_alive(self, game_list):
        if KEY_GOOMBA in game_list and KEY_FIREBALL in game_list:
            if game_list[KEY_GOOMBA].rect.centerx == game_list[KEY_FIREBALL].rect.centerx:
                del game_list[KEY_GOOMBA]
                del game_list[KEY_FIREBALL]

                game_list[KEY_MARIO].fire_fireball = False

    def display_sys_info(self):
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUsage = py.memory_info()[0]/2.**30