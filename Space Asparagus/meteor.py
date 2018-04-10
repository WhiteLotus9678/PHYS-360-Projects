# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 14:59:23 2018

@author: Will Yang
"""
import pygame, random
from vec2d import Vec2d

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, mass, scale):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Position vector
        self.pos = pos
        
        # Velocity vector, y-value is set to 150
        self.vel = Vec2d(0, 150)
        
        # Object mass
        self.mass = mass
        
        # Momentum vector
        self.mom = self.vel*self.mass
        
        # Force vector, y-value is a random integer from 50 to 500
        self.force = Vec2d(0, random.randrange(50, 250))
        
        # Image scale
        self.scale = scale
        
        # Image filename
        self.filename = ""
        
        # Load the image of the asparagus and draw the image
        self.set_image()
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    def update(self, dt, screen_width, screen_height):
        # Increase the momentum vector
        self.mom += self.force*dt
        
        # Change the velocity based on the new momentum vector
        self.vel.copy_in(self.mom/self.mass)
        
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
        # Load the image of the asparagus and draw the image
        self.set_image()
        
        # Reset sprite's position
        self.rect.y = random.randrange(-300, -40)
        self.rect.x = random.randrange(50, screen_width - 50)
        
        # Reset the object's position, velocity, momentum and force
        self.pos = Vec2d(self.rect.x, self.rect.y)
        self.vel = Vec2d(0,random.randrange(70, 100))
        self.mom = Vec2d(0,0)

    def set_image(self):
        # Random integer from 0 to 5
        rand_meteor = random.randint(0, 5)
        
        # Choose a different file image for the meteor(s) based on the random integer
        if rand_meteor == 0:
            self.filename = "SpaceAssets/Meteor1.png"
        elif rand_meteor == 1:
            self.filename = "SpaceAssets/Meteor2.png"
        elif rand_meteor == 2:
            self.filename = "SpaceAssets/Meteor3.png"
        elif rand_meteor == 3:
            self.filename = "SpaceAssets/Meteor4.png"
        elif rand_meteor == 4:
            self.filename = "SpaceAssets/Meteor5.png"
        else:
           self.filename = "SpaceAssets/Meteor6.png"
        
        raw_image = pygame.image.load(self.filename).convert_alpha()
        self.image = pygame.transform.scale(raw_image,
                                (int(raw_image.get_width() * self.scale),
                                 int(raw_image.get_height() * self.scale)))
        self.rect = self.image.get_rect()