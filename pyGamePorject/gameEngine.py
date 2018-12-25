import sys
import pygame

class game_engine(object):
    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        self.background_color = 0
        self.caption = ""

    def set_screen(self, width, height):
        self.screen_height = height
        self.screen_width  = width
    
    def set_background_color(self, background_color):
        self.background_color = background_color
    
    def set_caption(self, caption):
        self.caption = caption

    def update_screen(self):
        pass
    
    def respond_to_event(self):
        pass