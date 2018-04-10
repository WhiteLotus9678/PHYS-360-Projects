# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:38:52 2018

@author: Will Yang
"""

import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # Call Sprite initializer
        self.image = pygame.image.load(image_file) # Set background to image file
        self.rect = self.image.get_rect() # Extract the rect area out of the image
        self.rect.left, self.rect.top = location
        self.size = self.image.get_size() # Background size
        (w,h) = self.size # Extract the width and height of the image
        self.x = 0 # Top Left
        self.y = 0 # Top Left
        self.x1 = 0 # Bottom Left
        self.y1 = -h # Bottom Left
        self.height = h # Background height
    
    def update(self, screen):        
        # Move the background down 5 pixels
        self.y1 += 5
        self.y += 5
        
        # Redraw the background
        screen.blit(self.image,(self.x,self.y))
        screen.blit(self.image,(self.x1,self.y1))
        
        # Reset the background to its original position
        if self.y > self.height:
            self.y = -self.height
        if self.y1 > self.height:
            self.y1 = -self.height