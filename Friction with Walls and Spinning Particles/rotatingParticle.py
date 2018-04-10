# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:38:45 2018

@author: Cheenue Yaj, Will Yang, Trevor Kretschmann
"""
import pygame
import math
from vec2d import Vec2d
from particle import Particle

# This class is a child of Particle
class rotatingParticle(Particle):
    def __init__(self, pos, vel, mass, radius, color, coords, linecolor, angle = 0, angvel = 0):
        super().__init__(pos, vel, mass, radius, color, coords)
        self.angle = angle
        self.angvel = angvel
        self.moment = 0.5 * self.mass * self.radius * self.radius
        self.angmom = self.moment * self.angvel
        self.torque = 0
        self.linecolor = linecolor

    # Update the particle's momentum as the angular momentum changes
    def update_mom(self, dt):
        self.angmom += self.torque * dt
    
    def update_radius(self):
        super().update_radius()
    
    def update_vel(self):
        super().update_vel()
    
    # Update the particle's angular velocity as the angular momentim changes
    def update_angvel(self):
        self.angvel = self.angmom/self.moment
    
    def set_velocity(self, vel):
        super().set_velocity(vel)
    
    # Update the particle's position as the angular velocity changes over time
    def update_angle(self, dt):
        self.angle += self.angvel * dt
        
    def update(self, dt):
        super().update(dt)
    
    # Update the particle's momentum and angular momentumdue to the impulses on it
    def impulse(self, imp, point):
        self.mom += imp
        self.update_vel()
        self.angmom += (point - self.pos).cross(imp)
        self.update_angvel()
    
    # Draw the radius of the particle; it will rotate as the particle rotates
    def draw(self, screen, coords):
        super().draw(screen, coords)
        vec = self.radius * Vec2d(math.cos(self.angle), math.sin(self.angle))
        pygame.draw.line(screen, self.linecolor, coords.pos_to_screen(self.pos).int(),
                         coords.pos_to_screen(self.pos + vec).int())