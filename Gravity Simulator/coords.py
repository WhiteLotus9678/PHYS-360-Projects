# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
obj.mom -= vCOM * obj.mass
else change its velocity to 0
"""
from vec2d import Vec2d

class Coords:
    def __init__(self, origin=Vec2d(0,0), scale=1, yflip=False):
        self.scale = scale
        self.origin = origin
        self.yflip = yflip
        
    def scalar_to_screen(self, scalar):
        return self.scale*scalar

    def scalar_to_coords(self, scalar):
        return scalar/self.scale
    
    def pos_to_screen(self, pos):
        v = pos.copy()
        if self.yflip:
            v.y *= -1    
        return self.origin + self.scale*v
    
    def pos_to_coords(self, pos):
        v = (pos - self.origin)/self.scale
        if self.yflip:
            v.y *= -1
        return v
    
    def vec_to_screen(self, vec):
        v = self.scale*vec
        if self.yflip:
            v.y *= -1
        return v
     
    def vec_to_coords(self, vec):
        v = vec/self.scale
        if self.yflip:
            v.y *= -1
        return v

    def pan_in_screen(self, vec):
        self.origin -= vec

    def pan_in_coords(self, vec):
        v = self.vec_to_screen(vec)
        self.pan_in_screen(v)
        
    def zoom_at_screen(self, center, factor):
        self.origin -= center
        self.origin *= factor
        self.origin += center
        self.scale *= factor
    
    def zoom_at_coords(self, center, factor):
        c = self.pos_to_screen(center)
        self.zoom_at_screen(c, factor)
        
    def match_screen_and_coords(self, screen=Vec2d(0,0), coords=Vec2d(0,0)):
        v = self.scale*coords
        if self.yflip:
            v.y *= -1
        self.origin.copy_in(screen - v)
