# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d

class Rectangle:
    #particles.append(Particle(Vec2d(posx,posy), Vec2d(velx,vely), mass, radius, random_bright_color(), coords))
    #particles.append(Particle(Vec2d(posx,posy), Vec2d(0,0), 1, 0.25, 0.25, random_bright_color(), coords))
    def __init__(self, pos, vel, mass, width, height, color, coords):
        self.pos = coords.pos_to_coords(pos)
        self.vel = vel
        self.mass = mass
        self.width = width
        self.height = height
        self.color = color
        self.mom = self.vel*self.mass
        self.force = Vec2d(0,0)
        self.radius = width
    def update(self, dt):
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
                
    def draw(self, screen, coords):
        pygame.draw.rect(screen, self.color, pygame.Rect(coords.pos_to_screen(self.pos).int(),
            [coords.scalar_to_screen(self.width), coords.scalar_to_screen(self.height)]))
        #pygame.draw.rect(screen, GREEN, [0, height - 50, width, 50])