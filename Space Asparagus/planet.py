# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 22:34:46 2018

@author: Will Yang
"""
import pygame, random
from vec2d import Vec2d

class Planet(pygame.sprite.Sprite):
    def __init__(self, pos, mass, scale):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Position vector
        self.pos = pos
        
        # Velocity vector, y-value is set to 100
        self.vel = Vec2d(0, 100)
        
        # Object mass
        self.mass = mass
        
        # Momentum vector
        self.mom = self.vel*self.mass
        
        # No force, asparagi moves with constant velocity
        self.force = Vec2d(0,0)
        
        # Image scale
        self.scale = scale
        
        # Image filename
        self.filename = ""
        
        # Load the image of the asparagus and draw the image
        self.set_image()
        
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    def update(self, dt, screen_width, screen_height):        
        # Increase the position vector
        self.pos += self.vel*dt

        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
        # If block is too far down, reset to top of screen.
        if self.rect.y >= screen_height + 10:
            self.reset_pos(screen_width)

    """ Reset position to the top of the screen, at a random x location.
    Called by update() or the main program loop if there is a collision.
    """
    def reset_pos(self, screen_width):
        # Load the image of the asparagus and draw the image
        self.set_image()
        
        # Reset sprite's position
        self.rect.y = random.randrange(-300, -150)
        self.rect.x = random.randrange(200, screen_width - 210)
        
        # Reset the object's position, velocity, momentum and force
        self.pos = Vec2d(self.rect.x, self.rect.y)
        self.vel = Vec2d(0,random.randrange(70, 100))
        self.mom = Vec2d(0,0)
        self.force = Vec2d(0,0)

    def set_image(self):
        # Random integer from 0 to 2
        rand_planet = random.randint(0, 2)

        # Choose a different file image for the planet(s) based on the random integer
        if rand_planet == 0:
            self.filename = "SpaceAssets/MoonPlanet.png"
        elif rand_planet == 1:
            self.filename = "SpaceAssets/Planet1.png"
        else:
           self.filename = "SpaceAssets/Planet2.png"
        
        self.raw_image = pygame.image.load(self.filename).convert_alpha()
        self.image = pygame.transform.scale(self.raw_image,
                                (int(self.raw_image.get_width() * self.scale),
                                 int(self.raw_image.get_height() * self.scale)))
        self.rect = self.image.get_rect()