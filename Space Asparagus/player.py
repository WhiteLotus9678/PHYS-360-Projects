# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 18:16:47 2018

@author: Will Yang
"""

import pygame
from vec2d import Vec2d

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, vel, mass, screen_width, screen_height, filename, scale):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Position vector
        self.pos = Vec2d(screen_width / 2, screen_height / 2)
        
        # Velocity vector
        self.vel = vel
        
        # Object mass
        self.mass = mass
        
        # Momentum vector
        self.mom = self.vel*self.mass
        
        # No force to start with
        self.force = Vec2d(0,0)
        
        # Screen width
        self.scr_w = screen_width
        
        # Screen height
        self.scr_h = screen_height
        
        # Load the image of the player and draw the image
        self.filename = filename
        self.raw_image = pygame.image.load(self.filename).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image,
                                (int(self.raw_image.get_width() * scale),
                                 int(self.raw_image.get_height() * scale)))
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    def update(self, dt, coords, scale):
        # Increase the momentum vector
        self.mom += self.force*dt
        
        # Velocity vector
        self.vel.copy_in(self.mom/self.mass)
        
        # Increase the position vector
        self.pos += self.vel*dt
 
        # Set the rectangle object to be the same as the player's position
        pos_screen = coords.pos_to_screen(self.pos)
        self.rect.x = pos_screen.x
        self.rect.y = pos_screen.y
    
    def reset_pos(self, coords):
        # Reset momentum
        self.mom = Vec2d(0,0)
        
        # Reset force
        self.force = Vec2d(0,0)
        
        # Reset position
        self.pos = Vec2d(self.scr_w / 2, self.scr_h / 2)
        
        # Reset the rectangle object
        pos_screen = coords.pos_to_screen(self.pos)
        self.rect.x = pos_screen.x
        self.rect.y = pos_screen.y