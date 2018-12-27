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

class fire_ball(game_element):
    def __init__(self, screen):
        game_element.__init__(self, screen)
        self.frame_counter = 0
        self.image = {}
        self.rect  = None
        self.num_frames = 0
        self.direction = None

    def set_fire_ball_block(self, screen, frames):
        for index, frame in enumerate(frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            rect = img.get_rect()

            self.image[index] = img
            self.rect = rect
            self.screen_rect = screen.get_rect()
    
            self.rect.centerx = FLOWER_POSITION_X
            self.rect.centery = FLOWER_POSITION_Y

            self.num_frames = self.num_frames + 1
    
    def draw_fire_ball_block(self, screen, frame_counter):
        if frame_counter % 100 == 0:  
            self.frame_counter = self.frame_counter + 1            
        
        if self.frame_counter == self.num_frames:
            self.frame_counter = 0

        self.screen.blit(self.image[self.frame_counter], self.rect)

    def create_fire_ball_frames(self):
        fire_ball_frames = []
        current_path = pathlib.Path('./fire_ball_frames')
        current_pattern = "f*s.gif"
        
        for frame in current_path.glob(current_pattern):
            fire_ball_frames.append(frame)
        
        return fire_ball_frames
    
    def draw(self, screen, element_name, frame_counter):
        self.draw_fire_ball_block(screen, frame_counter)

    def set(self, screen, element_name, isGif):
        self.element_name = element_name
        
        if isGif is True:
            frames = self.create_fire_ball_frames()
        
        self.set_fire_ball_block(screen, frames)

class mashroom(game_element):
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

    def set_mashroom(self, screen):
        self.image = pygame.image.load("MagicMushroom.png")
        self.rect  = self.image.get_rect()

        self.rect.centerx = MASHROOM_POSITION_X
        self.rect.centery = MASHROOM_POSITION_Y

    def draw_mashroom(self, screen):
        self.screen.blit(self.image, self.rect)

    def set(self, screen, element_name, isGif):
        self.element_name = element_name    
        self.set_mashroom(screen)

    def draw(self, screen, element_name, frame_counter):
        self.draw_mashroom(screen)

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
    
            self.rect.centerx = FLOWER_POSITION_X
            self.rect.centery = FLOWER_POSITION_Y

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
        self.direction    = KEY_DIRECTION_RIGHT
        self.jump_done    = True
        self.doing_jump   = False
        self.doing_running = False
        self.doing_standing = True
        self.jump_direction = DIRECTION_UP
        self.just_born      = True
        self.is_in_trainsion = False

        self.eat_mashroom = False
        self.eat_flower   = False
        self.eat_done     = True

        self.frame_counter = 0
        self.frame_step_counter = 0
        self.flip_draw     = False
        self.has_eat_something = False

        self.fire_fireball = False

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
                self.rect.centery = MARIO_POSITION_Y_INIT

            self.num_frames = self.num_frames + 1
    
    def draw_mario_block(self, screen, frame_counter):
        if self.eat_done is True:
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
        elif self.eat_done is False:
            self.screen.blit(self.image[0], self.rect)

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

    def load_frames(self, current_pattern, current_path):
        self.num_frames = 0
        small_mario_frames = []

        for frame in current_path.glob(current_pattern):
            small_mario_frames.append(frame)
        
        for index, frame in enumerate(small_mario_frames):
            frame = ".\\" + str(frame)
            img  = pygame.image.load(frame)
            self.image[index] = img
            
            if self.eat_mashroom is True or self.eat_flower is True:
                current_x = self.rect.centerx
                
                if self.eat_done is False:
                    current_y = BIG_MARIO_POSITION_Y
                else:
                    current_y = self.rect.centery
            else:
                current_x = self.rect.centerx
                current_y = self.rect.centery
            
            self.rect.centerx = current_x
            self.rect.centery = current_y
            self.num_frames = self.num_frames + 1

    def update_mario_frames(self, screen):
        if self.doing_jump is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "S*M*J*.png"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "F*M*J*.png"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:  
                    current_pattern = "M*J*g.png"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
            elif self.direction == KEY_DIRECTION_LEFT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "S*M*J*Flip.png"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "F*M*J*Flip.png"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:    
                    current_pattern = "M*J*g*Flip.png"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
        elif self.doing_standing is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "S*M*S*.png"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "F*M*S*.png"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:    
                    current_pattern = "M*S*g.png"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
            elif self.direction == KEY_DIRECTION_LEFT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "S*M*S*Flip.png"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "F*M*S*Flip.png"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:    
                    current_pattern = "M*S*g*Flip.png"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
        elif self.doing_running is True:
            if self.direction == KEY_DIRECTION_RIGHT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "f*s.gif"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "f*s.gif"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:
                    current_pattern = "f*s.gif"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
            elif self.direction == KEY_DIRECTION_LEFT:
                if self.eat_mashroom is True and self.eat_flower is not True:
                    current_pattern = "f*s*p.gif"
                    current_path = pathlib.Path('./big_mario_frames')
                elif self.eat_flower is True:
                    current_pattern = "f*s*p.gif"
                    current_path = pathlib.Path('./fire_mario_frames')
                else:
                    current_pattern = "f*s*p.gif"
                    current_path = pathlib.Path('./small_mario_frames')
                self.load_frames(current_pattern, current_path)
    
    def update_mario_frames_grow(self, screen, draw_big):
        current_pattern = None
        current_path    = None
        if self.eat_mashroom is True and self.eat_flower is False:
            if draw_big is False:
                current_pattern = "M*S*g.png"
                current_path = pathlib.Path('./small_mario_frames')
            elif draw_big is True:
                current_pattern = "S*M*S*.png"
                current_path = pathlib.Path('./big_mario_frames')
            self.load_frames(current_pattern, current_path)
        elif self.eat_flower is True:
            #print("called")
            if draw_big is False:
                if self.eat_mashroom is True:
                    current_pattern = "S*M*S*.png"
                    current_path = pathlib.Path('./big_mario_frames')
                else:
                    current_pattern = "M*S*.png"
                    current_path = pathlib.Path('./small_mario_frames')
            elif draw_big is True:
                current_pattern = "F*M*S*.png"
                current_path = pathlib.Path('./fire_mario_frames')
            self.load_frames(current_pattern, current_path)
        else:
            pass

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

            self.rect[index].centerx = QUESTION_BLOCK_POSITION_X
            self.rect[index].centery = QUESTION_BLOCK_POSITION_Y

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