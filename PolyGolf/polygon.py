# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:26:03 2018

@author: sinkovitsd, Will Yang, Trevor Kretschmann, Cheenue Yang
"""

from math import sin, cos, degrees
from vec2d import Vec2d
import pygame

class Polygon:
    def __init__(self, pos, vel, density, points, color, angle=0, angvel=0):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.angle = angle
        self.angvel = angvel
        self.force = Vec2d(0,0)
        self.torque = 0
        self.type = "polygon"

        # Set origpoints
        self.origpoints = []
        for p in points:
            self.origpoints.append(p.copy())
        pp = self.origpoints

        # Tally area, moment, and center of mass
        self.area = 0
        self.moment = 0
        center = Vec2d(0,0)
        for i in range(len(pp)):
            # Area of triangle, and add to total area
            a = pp[i].cross(pp[i-1])/2
            self.area += a

            # Moment of triange about vertex
            I_vertex = (1/6) * density * a * (pp[i].mag() * pp[i].mag() + pp[i-1].mag() * pp[i-1].mag() + pp[i].dot(pp[i-1]))
            
            # Add center of mass of triange to center of mass of shape
            center += a*(pp[i] + pp[i-1])/3
            pass
        
        center *= 1/self.area
        if(self.area < 0):
            self.area *= -1
        self.mass = density*self.area

        # Shift self.origpoints to be centered on center of mass
        for p in self.origpoints:
            p -= center
        self.pos += center
        
        # Shift moment to be about center of mass (parallel axis theorem)
        self.moment += I_vertex - self.mass * self.pos.mag() * self.pos.mag()
        if(self.moment < 0):
            self.moment *= -1

        # Recalculate moment around the center of mass as a check
        moment = 0
        for i in range(len(pp)):
            # Same as above loop to tally moment of each triangle about vertex
            moment += (1/6) * density * a * (pp[i].mag() * pp[i].mag() + pp[i-1].mag() * pp[i-1].mag() + pp[i].dot(pp[i-1]))
            pass
        if(moment < 0):
            moment *= -1
        
        # Calculate normals to each points
        self.orignormals = []
        for i in range(len(pp)):
            # Calculate normal here and append to orignormals
            self.orignormals.append((pp[i-1] - pp[i]).perpendicular().hat())
            pass
        
        # Calculate rotated points and normals
        self.points = []
        for p in self.origpoints:
            self.points.append(Vec2d(0,0))
        self.normals = []
        for n in self.orignormals:
            self.normals.append(Vec2d(0,0))
        self.update_points_normals()
                
        self.mom = self.mass*self.vel
        self.angmom = self.moment*self.angvel
        
    def update_mom(self, dt):
        self.mom += self.force*dt
        self.angmom += self.torque*dt
        self.update_vel()
        self.update_angvel()
        
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
    
    def update_angvel(self):
        self.angvel = self.angmom/self.moment

    def update_pos(self, dt):
        self.pos += self.vel*dt
        self.angle += self.angvel*dt
        if self.angvel*dt != 0:
            self.update_points_normals()
            
    def update_points_normals(self):
        pp = self.origpoints
        pn = self.orignormals
        c = cos(self.angle)
        s = sin(self.angle)
        #> use s and c to calculate points and normals rotated
        for i in range(len(pp)):
            x = pp[i].x
            y = pp[i].y
            
            self.points[i].x = x*c - y*s
            self.points[i].y = y*c + x*s
        
        # Calculating normals
        for i in range(len(pn)):
            x = pn[i].x
            y = pn[i].y
            
            self.normals[i].x = x*c - y*s
            self.normals[i].y = y*c + x*s

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
                
    def impulse(self, imp, point=None):
        self.mom += imp
        self.update_vel()
        if point is not None:
            self.angmom += (point - self.pos).cross(imp)  
            self.update_angvel()

    def draw(self, screen, coords):
        # Draw polygon
        points = []
        for p in self.points:
            points.append(coords.pos_to_screen(self.pos + p))
        shape = pygame.draw.polygon(screen, self.color, points)
        if False:
            for i in range(len(points)):
                length = 50
                n = coords.unitvec_to_other(self.normals[i])
                p = (points[i] + points[i-1])/2
                pygame.draw.line(screen, (0,0,0), p, p + length*n)
        return shape
    
    """ Self supplies the vertices.  Other provides the sides (walls).
                For each wall, find the point that penetrates the MOST, 
                and record the magnitude of penetration.  If for one wall, 
                no point penetrates, there is no overlap; return False.
                Otherwise, find which wall is LEAST penetrated, and pass back,
                via result.extend(), the overlap, point and normal involved; 
                return True. 
    """
    def check_collision(self, other, result=[]):
        result.clear()
        overlap = 1e99
        r_other = Vec2d(0,0)
        r_self = Vec2d(0,0)
        d = 0
        n_hat = 0
        maxd = -1e99
        normal = 0
        point = None
        
        if self.type == "obstacle" and other.type == "wall":
            return
        elif other.type == "obstacle":
            points = other.points
            normals = other.normals
        elif other.type == "polygon":
            points = other.points
            normals = other.normals
        elif other.type == "wall":
            points = [Vec2d(0,0)]
            normals = [other.normal]
        else:
            return False
        
        for i in range(len(normals)):
            r_other = other.pos + points[i]
            n_hat = normals[i]
            maxd = -1e99
            pass
            for j in range(len(self.points)):
                r_self = self.pos + self.points[j]
                d = (r_other - r_self).dot(n_hat)
                if d > maxd:
                    maxd = d
                    maxpoint = r_self
            
            if maxd < overlap:
                if maxd < 1e-9: # catch floating point errors
                    return False
                overlap = maxd
                normal = n_hat
                point = maxpoint
        
        result.extend([self, other, overlap, normal, point])
        return True