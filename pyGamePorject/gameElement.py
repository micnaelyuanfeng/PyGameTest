import pygame
import pathlib

from macroDefines import *

class game_element(object):
    def __init__(self, screen):
        self.element_name = ""
        self.screen   = screen
        self.position = []
    
    def update_element(self):
        pass

    def create_element(self):
        pass

    def destroy_element(self):
        pass

    def get_element_name(self):
        return self.element_name

    def set_background(self, screen):
        self.image = pygame.image.load("Background.png")
        self.rect  = self.image.get_rect()

        self.image = pygame.transform.chop(self.image, (0, 240, 0, 0))

    def draw_background(self, screen):
        self.screen.blit(self.image, [0, 0])

    def set(self, screen, element_name, isGif):    

        self.set_background(screen)

    def draw(self, screen, element_name, frame_counter):
        self.draw_background(screen)

class mashroom(game_element):
    pass

class fire_flower(game_element):
    def __init__(self, screen):
        game_element.__init__(self, screen)
        self.frame_counter = 0
        self.image = {}
        self.rect  = None
        self.num_frames = 0

    def set_fire_flower_block(self, screen, frames):
        for index, frame in enumerate(frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            rect = img.get_rect()

            self.image[index] = img
            self.rect = rect
            self.screen_rect = screen.get_rect()
    
            self.rect.centerx = 150
            self.rect.centery = 199

            self.num_frames = self.num_frames + 1
    
    def draw_fire_flower_block(self, screen, frame_counter):
        if frame_counter % 100 == 0:  
            self.frame_counter = self.frame_counter + 1            
        
        if self.frame_counter == self.num_frames:
            self.frame_counter = 0

        self.screen.blit(self.image[self.frame_counter], self.rect)

    def create_fire_flower_frames(self):
        small_mario_frames = []
        current_path = pathlib.Path('./fire_flower_frames')
        current_pattern = "f*.gif"
        
        for frame in current_path.glob(current_pattern):
            small_mario_frames.append(frame)
        
        return small_mario_frames
    
    def draw(self, screen, element_name, frame_counter):
        self.draw_fire_flower_block(screen, frame_counter)

    def set(self, screen, element_name, isGif):
        self.element_name = element_name
        
        if isGif is True:
            frames = self.create_fire_flower_frames()
        
        self.set_fire_flower_block(screen, frames)

class mario_block(game_element):
    def __init__(self, screen):
        game_element.__init__(self, screen)
        self.frame_counter = 0
        self.image = {}
        self.rect  = None
        self.num_frames   = 0
        self.eat_mashroom = False
        self.eat_flower   = False
        self.direction    = KEY_DIRECTION_RIGHT
        self.jump_done    = True
        self.doing_jump   = False
        self.doing_running = False
        self.doing_standing = True
        self.jump_direction = DIRECTION_UP
        self.just_born      = True
        self.is_in_trainsion = False

    def set_mario_block(self, screen, frames):
        self.num_frames = 0

        for index, frame in enumerate(frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            rect = img.get_rect()
            self.image[index] = img
            self.rect = rect
            self.screen_rect = screen.get_rect()

            if self.just_born is True:
                self.just_born = False
                self.rect.centerx = MARIO_POSITION_X_INIT
                self.rect.centery = MATIO_POSITION_Y_INIT

            self.num_frames = self.num_frames + 1
    
    def draw_mario_block(self, screen, frame_counter):
        if self.doing_standing is True:
            self.screen.blit(self.image[0], self.rect)
        elif self.doing_jump is True:
            self.screen.blit(self.image[0], self.rect)
        elif self.doing_running is True:
            if frame_counter % 100 == 0:  
                self.frame_counter = self.frame_counter + 1          
            
            if self.frame_counter == self.num_frames:
                self.frame_counter = 0
            
            self.screen.blit(self.image[self.frame_counter], self.rect)
        else:
            pass

    def create_mario_frames(self):
        small_mario_frames = []
        current_path = pathlib.Path('./small_mario_frames')
        
        if self.doing_standing is True:
            current_pattern = "M*S*g.png"
        elif self.doing_running is True:
            current_pattern = "f*s.gif"
        
        for frame in current_path.glob(current_pattern):      
            small_mario_frames.append(frame)
        
        return small_mario_frames
    
    def draw(self, screen, element_name, frame_counter):
        self.draw_mario_block(screen, frame_counter)

    def set(self, screen, element_name, isGif):
        self.element_name = element_name
        
        if isGif is True:
            frames = self.create_mario_frames()
        
        self.set_mario_block(screen, frames)

    def load_frames(self, current_pattern):
        self.num_frames = 0
        small_mario_frames = []

        current_path = pathlib.Path('./small_mario_frames')

        for frame in current_path.glob(current_pattern):
            small_mario_frames.append(frame)
        
        for index, frame in enumerate(small_mario_frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            self.image[index] = img
            
            current_x = self.rect.centerx
            current_y = self.rect.centery
            
            self.rect.centerx = current_x
            self.rect.centery = current_y
            self.num_frames = self.num_frames + 1

    def update_mario_frames(self, screen):
        if self.doing_jump is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                current_pattern = "M*J*g.png"
                self.load_frames(current_pattern)
            elif self.direction == KEY_DIRECTION_LEFT:
                current_pattern = "M*J*g*Flip.png"
                self.load_frames(current_pattern)
        elif self.doing_standing is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                current_pattern = "M*S*g.png"
                self.load_frames(current_pattern)
            elif self.direction == KEY_DIRECTION_LEFT:
                current_pattern = "M*S*g*Flip.png"
                self.load_frames(current_pattern)
        elif self.doing_running is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                current_pattern = "f*s.gif"
                self.load_frames(current_pattern)
            elif self.direction == KEY_DIRECTION_LEFT:
                current_pattern = "f*s*p.gif"
                self.load_frames(current_pattern)

class question_block(game_element):
    def __init__(self, screen):
        game_element.__init__(self, screen)
        self.frame_counter = 0
        self.image = {}
        self.rect  = {}
        self.num_frames = 0
 
    def set_question_block(self, screen, frames):
        for index, frame in enumerate(frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            rect = img.get_rect()

            self.image[index] = img
            self.rect[index] = rect

            self.num_frames = self.num_frames + 1

    def draw_question_block(self, screen, frame_counter):
        if frame_counter % 100 == 0:  
            self.frame_counter = self.frame_counter + 1            
        
        if self.frame_counter == self.num_frames:
            self.frame_counter = 0
        
        self.screen.blit(self.image[self.frame_counter], self.rect[self.frame_counter])

        
    def create_qb_frames(self):
        qb_frames = []
        current_path = pathlib.Path('./question_block_frames')
        current_pattern = "f*.gif"
        
        for frame in current_path.glob(current_pattern):
            qb_frames.append(frame)
        
        return qb_frames

    def draw(self, screen, element_name, frame_counter):
        self.draw_question_block(screen, frame_counter)

    def set(self, screen, element_name, isGif):
        self.element_name = element_name
        
        if isGif is True:
            frames = self.create_qb_frames()
        
        self.set_question_block(screen, frames)

class turtle_block(game_element):
    pass

class goomba_block(game_element):
    def __init__(self, screen):
        game_element.__init__(self, screen)
        self.frame_counter = 0
        self.image = {}
        self.rect = None
        self.num_frames = 0
        self.direction = DIRECTION_LEFT
 
    def set_goomba_block(self, screen, frames):
        for index, frame in enumerate(frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            rect = img.get_rect()

            self.image[index] = img
            self.rect = rect
            self.screen_rect = screen.get_rect()
    
            self.rect.centerx = GOOMBA_1_POSITION_X_INIT
            self.rect.centery = GOOMBA_1_POSITION_Y_INIT
            self.num_frames = self.num_frames + 1

    def draw_goomba_block(self, screen, frame_counter):
        if frame_counter % 100 == 0:  
            self.frame_counter = self.frame_counter + 1            
        
        if self.frame_counter == self.num_frames:
            self.frame_counter = 0
        
        self.screen.blit(self.image[self.frame_counter], self.rect)

        
    def create_goomba_frames(self):
        qb_frames = []
        current_path = pathlib.Path('./little_goomba_frames')
        current_pattern = "f*.gif"
        
        for frame in current_path.glob(current_pattern):
            qb_frames.append(frame)
        
        return qb_frames

    def draw(self, screen, element_name, frame_counter):
        self.draw_goomba_block(screen, frame_counter)

    def set(self, screen, element_name, isGif):
        self.element_name = "goombaBlock"
        
        if isGif is True:
            frames = self.create_goomba_frames()
        
        self.set_goomba_block(screen, frames)