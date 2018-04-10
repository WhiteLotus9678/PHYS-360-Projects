# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:34:32 2018

@author: Will Yang
"""
import pygame, random
from vec2d import Vec2d

class Asparagus(pygame.sprite.Sprite):
    def __init__(self, pos, mass, filename, scale):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Position vector
        self.pos = pos
        
        # Velocity vector, y-value is a random integer from 200 to 250
        self.vel = Vec2d(0,random.randrange(200, 250))
        
        # Object mass
        self.mass = mass
        
        # Momentum vector
        self.mom = self.vel*self.mass
        
        # No force, asparagi moves with constant velocity
        self.force = Vec2d(0, 0)
        
        # Load the image of the asparagus and draw the image
        self.filename = filename # Name of the image file
        self.raw_image = pygame.image.load(self.filename).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image,
                                (int(self.raw_image.get_width() * scale),
                                 int(self.raw_image.get_height() * scale)))
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    def update(self, dt, screen_width, screen_height):
        # Increase the position vector
        self.pos += self.vel*dt

        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
        # If block is too far down, reset to top of screen
        if self.rect.y >= screen_height + 10:
            self.reset_pos(screen_width)

    """ Reset position to the top of the screen, at a random x location.
    Called by update() or the main program loop if there is a collision.
    """
    def reset_pos(self, screen_width):
        # Reset sprite's position
        self.rect.y = random.randrange(-300, -40)
        self.rect.x = random.randrange(0, screen_width - 10)
        
        # Reset the object's position and momentum
        self.pos = Vec2d(self.rect.x, self.rect.y)
        self.vel = Vec2d(0,random.randrange(150, 200))
        self.mom = Vec2d(0,0)