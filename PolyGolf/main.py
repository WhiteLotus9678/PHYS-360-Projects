# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd, Will Yang, Trevor Kretschmann, Cheenue Yang
"""
import pygame
from vec2d import Vec2d
from coords import Coords
from polygon import Polygon
from wall import Wall
from math import sqrt, acos, degrees, sin, cos
from random import uniform, randint, random

GRASS = pygame.image.load("field.jpg")

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
DARKBLUE     = (   0,   0, 100)
GRAY     = ( 127, 127, 127)

def random_color():
    return (randint(0,255), randint(0,255), randint(0,255))

def random_bright_color():
    i = randint(0,2)
    d = randint(1,2)
    c = int(256*random()**0.5)
    color = [0,0,0]
    color[i] = 255
    color[(i+d)%3] = c
    return color

def make_polygon(radius, n, angle=0, factor=1, axis=Vec2d(1,0)):
    axis = axis.normalized()
    vec = Vec2d(0, -radius).rotated(180/n+angle)
    p = []
    for i in range(n):
        v = vec.rotated(360*i/n)
        v += v.dot(axis)*(factor-1)*axis
        p.append(v)
    return p

def make_rectangle(length, height, angle=0):
    points = (Vec2d(-0.5,-0.5),
              Vec2d(+0.5,-0.5),
              Vec2d(+0.5,+0.5),
              Vec2d(-0.5,+0.5),
              )
    c = cos(angle)
    s = sin(angle)
    for p in points:
        p.x *= length
        p.y *= height
        x = p.x*c - p.y*s
        y = p.y*c + p.x*s
        p.x = x
        p.y = y
    return points

# Draw a particle's velocity line
def make_velocity_line():
    
    # Default velocity line value
    velVec = Vec2d(0,0)
    
    # Get mouse position
    mouse = (posx, posy) = pygame.mouse.get_pos()
    
    # Object's position
    obj = coords.pos_to_screen(objects[ballIndex].pos)
    
    # Distance between the ball and mouse
    d = obj - Vec2d(mouse)
    
    # Draw the line from the circle and away from the mouse
    pygame.draw.line(screen, GREEN, obj, Vec2d(mouse), 5)
     
    # Calculate the velocity using the distance between the particle center and endpoint   
    velVec.x = posx - obj.x
    velVec.y = obj.y - posy

    return velVec

def make_putting_line():
    
    # Default velocity line value
    velVec = Vec2d(0,0)
    
    # Get mouse position
    mouse = (posx, posy) = pygame.mouse.get_pos()
    
    # Object's position
    obj = coords.pos_to_screen(objects[ballIndex].pos)
    
    # Draw the line from the circle and away from the mouse
    pygame.draw.line(screen, BLACK, obj, Vec2d(mouse), 1)
    return velVec

def check_collision(a, b, result=[]):
    result.clear()
    result1 = []
    result2 = []
    if a.check_collision(b, result1) and b.check_collision(a, result2):
        if result1[2] < result2[2]: # Compare overlaps, whichever one is smaller
            result.extend(result1)
        else:
            result.extend(result2)
        return True
    return False       

def resolve_collision(result):
    (a, b, d, n, pt) = result # self, other, overlap, normal, point
    e = 0.95 # coefficient of elasticity
    mu = 0.8 # 0.4
    m = a.mass*b.mass/(a.mass + b.mass) # reduced mass
    t = n.perpendicular() # t is translational, perpendicular to normal
    s = 0
    
    # Depenetration
    a.pos += d*n*m/a.mass
    pt += d*n*m/a.mass
    b.pos -= d*n*m/b.mass # TO DO - this might make them move in the same direction

    # Distance Vectors
    r1 = pt - a.pos
    r2 = pt - b.pos
    r1n = r1.dot(n)
    r1t = r1.dot(t)
    r2n = r2.dot(n)
    r2t = r2.dot(t)
    
    # Relative velocity of points in contact
    v_rel = (a.vel + (a.angvel*a.pos.perpendicular())) - (b.vel + (b.angvel*b.pos.perpendicular()))
    
    # Target velocity change (delta v)
    delta_vn = -(1+e)*v_rel.dot(n)
    delta_vt = -v_rel.dot(t)
    
    # Matrix [[A B][C D]] [Jn Jt]T = [dvn dvt]T
    A = (1/a.mass)+(r1t*r1t/a.moment) + (1/b.mass)+(r2t*r2t/b.moment)
    B = -(r1n*r1t/a.moment) - (r2n*r2t/b.moment)
    C = B
    D = (1/a.mass)+(r1n*r1n/a.moment) + (1/b.mass)+(r2n*r2n/b.moment)
    
    # Solve matrix equation
    det = A*D - B*C
    
    # Check if friction is strong enough to prevent slipping
    # Check if moving toward one another
    # If not, no collision
    if (delta_vn > 0):
        #Perfect friction
        Jn = (1/det) * ((D * delta_vn) - (B * delta_vt))
        Jt = (1/det) * ((-C * delta_vn) + (A * delta_vt))
        
        # Check if Jt is too big for u
        # Friction not strong enough to prevent sliding
        if (abs(Jt) > (mu*Jn)):
            # Sliding friction
            if (Jt > 0):
                s = 1
            elif (Jt < 0):
                s = -1
            
            # Solve new matrix equation
            delta_vt = 0
            C = -s*mu
            D = 1
            det = A*D - B*C
            
            Jn = (1/det) * ((D * delta_vn) - (B * delta_vt))
            Jt = s * mu * Jn
        
        # Calculate and add impulses to each object
        J = Jn*n + Jt*t
        a.impulse( J, pt)
        b.impulse(-J, pt)

def main():
    global objects, screen, coords, ballIndex
    
    pygame.init()
 
    width = 1200
    height = 600
    screen = pygame.display.set_mode([width,height])
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    zoom = 100
    coords.zoom_at_coords(Vec2d(0,0), zoom) 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Text font
    basic_font = pygame.font.Font('freesansbold.ttf', 24)
    large_font = pygame.font.Font('freesansbold.ttf', 48)
    
    # Pause Text
    intro_surf = large_font.render('READY', True, GREEN)
    intro_rect = intro_surf.get_rect()
    intro_rect.center = (width / 2, (height * 0.4))
    
    # Strokes text
    stroke_surf = basic_font.render('Stroke: 0', True, WHITE)
    stroke_rect = stroke_surf.get_rect()
    stroke_rect.center = (width / 2, (height * 0.05))
    
    # Stage 1 Strokes Text
    stage1_surf = basic_font.render('Stage 1: 0 hits', True, RED)
    stage1_rect = stage1_surf.get_rect()
    stage1_rect.center = (100, height - 20)
    
    # Stage 2 Strokes Text
    stage2_surf = basic_font.render('Stage 2: 0 hits', True, RED)
    stage2_rect = stage2_surf.get_rect()
    stage2_rect.center = (250, height - 20) 
    
    # Stage 3 Strokes Text
    stage3_surf = basic_font.render('Stage 3: 0 hits', True, RED)
    stage3_rect = stage3_surf.get_rect()
    stage3_rect.center = (400, height - 20)     

    # Create initial objects to demonstrate
    objects = []

    # Goal
    goalRadius = 0.12
    objects.append(Polygon(Vec2d(-5,2), Vec2d(0,0), 1, make_polygon(goalRadius,36,0,1), BLACK, 0, 0))
    objects[-1].type = "goal"
    
    # Golf ball
    objects.append(Polygon(Vec2d(5,2), Vec2d(0,0), 1, make_polygon(0.1,36,0,1), WHITE, 0, 0))
    ballIndex = len(objects) - 1
    
    # Surrounding walls
    objects.append(Wall(coords.pos_to_coords(Vec2d(0, screen.get_height())), Vec2d(0, 1), BLACK)) # Bottom
    objects.append(Wall(coords.pos_to_coords(Vec2d(0, 0)), Vec2d(0, -1), BLACK)) # Top
    objects.append(Wall(coords.pos_to_coords(Vec2d(0, 0)), Vec2d(1, 0), BLACK)) # Left
    objects.append(Wall(coords.pos_to_coords(Vec2d(screen.get_width(), 0)), Vec2d(-1, 0), BLACK)) # Right
    
    # Triangle walls
    triangle1 = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.25, 0)), Vec2d(0,0), 999999, make_polygon(3,3,180,0.5), BLACK, 0, 0)
    triangle2 = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.50, screen.get_height())), Vec2d(0,0), 999999, make_polygon(3,3,0,0.5), BLACK, 0, 0)
    triangle3 = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.75, 0)), Vec2d(0,0), 999999, make_polygon(3,3,180,0.5), BLACK, 0, 0)
    
    triangle1.type = "obstacle"
    triangle2.type = "obstacle"
    triangle3.type = "obstacle"
    objects.append(triangle1)
    objects.append(triangle2)
    objects.append(triangle3)
    
    # Smaller spinning obstacle
    spinningLine1 = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.5, screen.get_height() * 0.25)), Vec2d(0, 0), 5, make_rectangle(1, 0.1), DARKBLUE, 0, 1)
    spinningLine1.type = "obstacle"
    objects.append(spinningLine1)
    
    # Larger spinning obstacle
    spinningLine2 = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.75, screen.get_height() * 0.75)), Vec2d(0, 0), 50, make_rectangle(2, 0.1), DARKBLUE, 0, 5)
    spinningLine2.type = "obstacle"
    objects.append(spinningLine2)
    
    # Small obstacles
    pentaObstacle = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.2, screen.get_height() * 0.4)), Vec2d(0, 0), 1, make_polygon(0.1, 5, 0, 1), DARKBLUE, 0, 0)
    pentaObstacle.type = "obstacle"
    objects.append(pentaObstacle)
    pentaObstacle = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.15, screen.get_height() * 0.4)), Vec2d(0, 0), 1, make_polygon(0.1, 5, 0, 1), DARKBLUE, 0, 0)
    pentaObstacle.type = "obstacle"
    objects.append(pentaObstacle)
    pentaObstacle = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.1, screen.get_height() * 0.4)), Vec2d(0, 0), 1, make_polygon(0.1, 5, 0, 1), DARKBLUE, 0, 0)
    pentaObstacle.type = "obstacle"
    objects.append(pentaObstacle)
    pentaObstacle = Polygon(coords.pos_to_coords(Vec2d(screen.get_width() * 0.05, screen.get_height() * 0.4)), Vec2d(0, 0), 1, make_polygon(0.1, 5, 0, 1), DARKBLUE, 0, 0)
    pentaObstacle.type = "obstacle"
    objects.append(pentaObstacle)
    
    # -------- Main Program Loop -----------\
    frame_rate = 60
    n_per_frame = 10
    playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
    dt = playback_speed/frame_rate/n_per_frame
    done = False
    paused = True
    draw = False
    goalScored = False
    max_collisions = 1
    result = []
    
    # Strokes
    strokeNumber = 0
    stage1Stroke = 0
    stage2Stroke = 0
    stage3Stroke = 0
    
    # Stage completion
    winStage1 = False
    winStage2 = False
    winStage3 = False
    
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                paused = True
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                #paused = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    done = True
                    paused = True 
                elif event.key == pygame.K_SPACE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if (objects[ballIndex].draw(screen, coords)).collidepoint(pos):
                        draw = True
            
            # Mouse Button Down Inputs
            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                # Assign mouse buttons
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                
            elif event.type == pygame.MOUSEBUTTONUP and paused:
                # Assign mouse buttons
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                
                # Mouse left press to draw a particle
                if pressed1 == 0 and paused == True:                    
                    # The velocity line can be drawn
                    if draw:
                        strokeNumber += 1
                    draw = False
                    paused = False

        if not paused:
            # Stroke Text
            # If the polygon ball has stopped, allow the user to hit it again
            if(objects[ballIndex].vel.mag() <= 0.05):
                paused = True
            for N in range(n_per_frame):
                # Physics
                # Calculate the force on each object
                for obj in objects:
                    obj.force.zero()
                    obj.force += -1 * obj.vel * obj.mass
                    
                    # Slow down the ball
                    if obj.type == "polygon":
                        obj.torque = -0.75 * obj.angvel
                        pass

                # Move each object according to physics
                for obj in objects:
                    obj.update(dt)
                    
                for i in range(max_collisions):
                    collided = False
                    for i1 in range(len(objects)):
                        for i2 in range(i1):
                            if check_collision(objects[i1], objects[i2], result):
                                resolve_collision(result)
                                collided = True
                    if not collided: # if all collisions resolved, then we're done
                        break
                
                # Check distance between ball and goal
                goalDistanceVec = objects[0].pos - objects[ballIndex].pos
                goalDistance = goalDistanceVec.mag()
                if goalDistance < goalRadius * 0.95 and objects[ballIndex].vel.mag() < 3:
                    objects[ballIndex].pos = Vec2d(5,2) # set ball position to start position
                    stage1Stroke = strokeNumber
                    strokeNumber = 0
                    winStage1 = True
            
            # Drawing
            screen.fill(WHITE) # wipe the screen
            for y in range (0, 10):
                for x in range (0, 10):
                    screen.blit(GRASS, (x * 346, y * 346))
                    
            for obj in objects:
                obj.draw(screen, coords) # draw object to screen
                
            # Show stroke text
            stroke_surf = basic_font.render('Stroke: ' + str(strokeNumber), True, WHITE)
            screen.blit(stroke_surf, stroke_rect)
            
            # Show each stages' stroke text
            if(winStage1):
                stage1_surf = basic_font.render('Stage 1: ' + str(stage1Stroke), True, WHITE)
                screen.blit(stage1_surf, stage1_rect)
            if(winStage2):
                stage2_surf = basic_font.render('Stage 2: ' + str(stage2Stroke), True, WHITE)
                screen.blit(stage2_surf, stage2_rect)
            if(winStage3):
                stage3_surf = basic_font.render('Stage 3: ' + str(stage3Stroke), True, WHITE)
                screen.blit(stage3_surf, stage3_rect)
            
            # --- Update the screen with what we've drawn.
            pygame.display.update()
            
            # This limits the loop to the specified frame rate
            clock.tick(frame_rate)
        elif paused:
            for N in range(n_per_frame):
                # Physics
                # Move each object according to physics
                for obj in objects:
                    if obj != objects[ballIndex]:
                        obj.update(dt)
            # Drawing
            screen.fill(WHITE) # wipe the screen
            for y in range (0, 10):
                for x in range (0, 10):
                    screen.blit(GRASS, (x * 346, y * 346))
            
            for obj in objects:
                obj.draw(screen, coords) # draw object to screen
            if draw:
                objects[ballIndex].set_vel(make_velocity_line() / 35)
            
            # Show the pause text
            screen.blit(intro_surf, intro_rect)
            
            # Show stroke text
            stroke_surf = basic_font.render('Stroke: ' + str(strokeNumber), True, WHITE)
            screen.blit(stroke_surf, stroke_rect)
            
           # Show each stages' stroke text
            if(winStage1):
                stage1_surf = basic_font.render('Stage 1: ' + str(stage1Stroke), True, WHITE)
                screen.blit(stage1_surf, stage1_rect)
            if(winStage2):
                stage2_surf = basic_font.render('Stage 2: ' + str(stage2Stroke), True, WHITE)
                screen.blit(stage2_surf, stage2_rect)
            if(winStage3):
                stage3_surf = basic_font.render('Stage 3: ' + str(stage3Stroke), True, WHITE)
                screen.blit(stage3_surf, stage3_rect)
    
            # --- Update the screen with what we've drawn.
            pygame.display.update()
            
            # This limits the loop to the specified frame rate
            clock.tick(frame_rate)

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
