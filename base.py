import os
import pygame

class Base:
    BASE_IMG =pygame.transform.scale2x((pygame.image.load(os.path.join("assets","base.png" )))) 
    VEL = 3

    def __init__(self,y):
        self.WIDTH = self.BASE_IMG.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win): 
        win.blit(self.BASE_IMG, (self.x1, self.y))
        win.blit(self.BASE_IMG, (self.x2, self.y))
