# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:26:03 2018

@author: sinkovitsd, Will Yang
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
        print("origpoints =", self.origpoints)
        pp = self.origpoints # pp as an alternate label for this function

        # Tally area, moment, and center of mass
        self.area = 0
        self.moment = 0
        center = Vec2d(0,0)
        for i in range(len(pp)):
            #> area of triangle, and add to total area
            # A = .5 * r1 x r2
            # r1 = pp[i]
            # r2 = pp[i=1]
            # a = fabs(pp[i].cross(pp[i-1])/2)
            a = pp[i].cross(pp[i-1])/2
            self.area += a
            
            """
            Parallel Axis Theorem -->
            I other = I center + M abs(r)^2
            """
            #> moment of triange about vertex
            # m = density * area
            # density * area / 6
            # I_vertex = (1/6) * density * self.area * (abs(pp[i]) * abs(pp[i]) + abs(pp[i-1]) * abs(pp[i-1]) + pp[i].dot(pp[i-1]))
            I_vertex = (1/6) * density * a * (pp[i].mag() * pp[i].mag() + pp[i-1].mag() * pp[i-1].mag() + pp[i].dot(pp[i-1]))
            
            #> add center of mass of triange to center of mass of shape
            center += a*(pp[i] + pp[i-1])/3
            pass
        
        center *= 1/self.area
        if(self.area < 0):
            self.area *= -1
        self.mass = density*self.area
        print("center =", center)
        print("area =", self.area)
        print("mass =", self.mass)

        # Shift self.origpoints to be centered on center of mass
        for p in self.origpoints:
            p -= center
        self.pos += center
        
        #> Shift moment to be about center of mass (parallel axis theorem)
        self.moment += I_vertex - self.mass * self.pos.mag() * self.pos.mag()
        if(self.moment < 0):
            self.moment *= -1

        print("moment =", self.moment)
        #print(pp)

        # Recalculate moment around the center of mass as a check
        moment = 0
        for i in range(len(pp)):
            #> same as above loop to tally moment of each triangle about vertex
            moment += (1/6) * density * a * (pp[i].mag() * pp[i].mag() + pp[i-1].mag() * pp[i-1].mag() + pp[i].dot(pp[i-1]))
            # tmpmom
            pass
        if(moment < 0):
            moment *= -1    
        print("moment =", moment)
        
        # Calculate normals to each points
        self.orignormals = []
        for i in range(len(pp)):
            #> calculate normal here and append to orignormals
            self.orignormals.append((pp[i-1] - pp[i]).perpendicular().hat()) #perpendicular_normal()
            pass
        print("orignormals =", self.orignormals)
        
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
        #print("points =", self.points)
        #print("normals =", self.normals)
        
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
    
    """
    distance_n = distance * n_hat
    dustance_t = distance * t_hat
    
    delta_v_n = ((1 / self.mass) + ((distance_t * distance_t) / self.moment)) * impulse_n - ((distance_n * distance_t) / self.moment) * impulse_t
    FIX: delta_v_t = ((1 / self.mass) + ((distance_t * distance_t) / self.moment)) * impulse_n - ((distance_n * distance_t) / self.moment) * impulse_t
    """

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
        "Rotating counter clockwise by angle theta"
        "xPrime = x*cos(theta) - y*sin(theta)"
        "yPrime = y*cos(theta) + x*sin(theta)"

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
                
    def impulse(self, imp, point=None):
        self.mom += imp
        self.update_vel()
        if point is not None:
            self.angmom += (point - self.pos).cross(imp)  
            self.update_angvel()
    """
    def draw(self, screen, coords):
        # Draw polygon
        for i, p in enumerate(self.points):
            self.scaledpoints[i].copy_in(coords.pos_to_screen(self.pos + p))
        #print(self.scaledpoints)
        pygame.draw.polygon(screen, self.color, self.scaledpoints)
        for i in range(len(self.scaledpoints)):
            length = 50
            n = coords.unitvec_to_other(self.normals[i])
            p = (self.scaledpoints[i] + self.scaledpoints[i-1])/2
            pygame.draw.line(screen, (0,0,0), p, p + length*n)
    """
    def draw(self, screen, coords):
        # Draw polygon
        points = []
        for p in self.points:
            points.append(coords.pos_to_screen(self.pos + p))
        pygame.draw.polygon(screen, self.color, points, 2)
        if True:
            for i in range(len(points)):
                length = 50
                n = coords.unitvec_to_other(self.normals[i])
                p = (points[i] + points[i-1])/2
                pygame.draw.line(screen, (0,0,0), p, p + length*n)
                #print("p: ", p)
    
    
    """ Self supplies the vertices.  Other provides the sides (walls).
                For each wall, find the point that penetrates the MOST, 
                and record the magnitude of penetration.  If for one wall, 
                no point penetrates, there is no overlap; return False.
                Otherwise, find which wall is LEAST penetrated, and pass back,
                via result.extend(), the overlap, point and normal involved; 
                return True. 
    """
                
    """ collision

            1. find point of maximum penetration
            d is the same as the wall
            penetration point = self.pos + point
            
            if no penetration, immediately return false
            
            2. looking at the other sides, find that point of maximum penetration
            3. Return whichever side that gives the minimum penetration
            
    """
    def check_collision(self, other, result=[]):
        result.clear() # See polygon_collision_test.py in check_collision()
        overlap = 1e99
        r_other = Vec2d(0,0)
        r_self = Vec2d(0,0)
        d = 0
        n_hat = 0
        maxd = -1e99
        #maxj = 0
        normal = 0
        point = None
        
        if other.type == "polygon":            
            
            for i in range(len(other.normals)):
                # Fill in
                r_other = other.pos + other.points[i]
                n_hat = other.normals[i]
                maxd = -1e99
                pass
                for j in range(len(self.points)):
                    # Fill in
                    r_self = self.pos + self.points[j]
                    d = (r_other - r_self).dot(n_hat)
                    if d > maxd:
                        maxd = d
                        #maxj = j
                        maxpoint = r_self
            
                print(self.color, maxd, n_hat)
                
                if maxd < overlap:
                    if maxd < 1e-9: # catch floating point errors
                        return False
                    overlap = maxd
                    normal = n_hat
                    #point = self.pos + self.points[maxj]
                    point = maxpoint
            result.extend([self, other, overlap, normal, point])
            return True