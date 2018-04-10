# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:02:42 2018

@author: Will Yang
"""
import pygame
from vec2d import Vec2d

class Particle:
    def __init__(self, pos, vel, mass, radius, color, coords):
        
        # Particle position i ncoordinates
        self.pos = coords.pos_to_coords(pos)
        
        # Particle velocity
        self.vel = vel
        
        # Particle mass
        self.mass = mass
        
        # Particle radius
        self.radius = radius
        
        # Particle color
        self.color = color
        
        # Momentum
        self.mom = self.vel*self.mass
        
        # Force
        self.force = Vec2d(0,0)
        
        #
        self.type = "particle"
        
        #
        self.wallTouch = False
        
    # The mass is proportional to the radius^2 multiplied by the ratio of mass/radius (1/0.25) which is 16
    def update_radius(self):
        self.radius = self.radius
        self.mass = 16 * self.radius**2
    
    # Update the particle's velocity
    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
    
    # Method to help keep the velocity consistent
    def set_velocity(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)
    
    # Update the particle's physics
    def update(self, dt):
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
    
    # Draw the particle according to its color and position
    def draw(self, screen, coords):
        pygame.draw.circle(screen, self.color, 
                           coords.pos_to_screen(self.pos).int(), 
                           int(coords.scalar_to_screen(self.radius)), 0)