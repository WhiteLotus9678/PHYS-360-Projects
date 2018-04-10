# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:38:45 2018

@author: Cheenue Yaj, Will Yang, Trevor Kretschmann
"""
# Import some modules
import pygame
from vec2d import Vec2d
from coords import Coords
from rotatingParticle import rotatingParticle
from random import randint, random
from wall import Wall

# Gravity constant
gravityConstant = 9.8

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

# Generate random bright colors
def random_bright_color():
    i = randint(0,2)
    d = randint(1,2)
    c = int(256 * random()**0.5)
    color = [0,0,0]
    color[i] = 255
    color[(i+d)%3] = c
    
    return color

# Shift all particles by the center of mass (COM)
def shift_rCOM(particles):
    # rCOM = [ Σ(m*r) / Σ(m) ]
    numerator = 0
    denominator = 0
    rCOM = Vec2d(0,0)
    
    # Calculate the numerator and denominator using the particles' mass and position
    for particle in particles:
        if particle.type == "particle":
            numerator += (particle.mass * particle.pos)
            denominator += particle.mass

    # Calculate the COM using the numerator and denominator
    rCOM = numerator / denominator
    
    # Shift all particles by the same displacement so that the center of mass is at the origin
    for particle in particles:
        if particle.type == "particle":
            particle.pos -= rCOM

# Change the velocity of the center of mass (vCOM) to 0
def change_vCOM(particles):
    # vCOM = [ Σ(m*v) / Σ(m)]
    numerator = 0
    denominator = 0
    vCOM = Vec2d(0,0)
    
    # Calculate the numerator and denominator using the particles' mass and velocity
    for particle in particles:
        if particle.type == "particle":
            numerator += (particle.mass * particle.vel)
            denominator += particle.mass
    
    # Calculate the vCOM using the numerator and denominator
    vCOM = numerator / denominator
    
    # Subtract the vCOM from all particle's velocities so that the vCOM is zero
    for particle in particles:
        if particle.type == "particle":
            particle.set_velocity(particle.vel - vCOM)

# Receive all keyboard/mouse button inputs and execute
def getInput(coords):
    global RUNNING, particle_center, DRAW, PAUSE, count, particles
    
    for event in pygame.event.get():
            # Exit the Game
            if event.type == pygame.QUIT:
                RUNNING = False
            
            # Keyboard Inputs
            if event.type == pygame.KEYDOWN:
                
                # Pause/Unpause the game
                if event.key == pygame.K_SPACE and PAUSE == False:
                    PAUSE = True
                    DRAW = False
                elif event.key == pygame.K_SPACE and PAUSE == True:
                    PAUSE = False
                
            # For these inputs the game must be unpaused
                # Press 0 to calculate the COM and vCOM
                if event.key == pygame.K_0 and PAUSE == False:
                    shift_rCOM(particles)
                    change_vCOM(particles)
                
                # Zoom Out
                if event.key == pygame.K_EQUALS and PAUSE == False:
                    coords.zoom_at_coords(Vec2d(0,0), 1.1)
                    
                # Zoom In
                if event.key == pygame.K_MINUS and PAUSE == False:
                    coords.zoom_at_coords(Vec2d(0,0), 0.9)
                
                # Pan Left                    
                if event.key == pygame.K_LEFT and PAUSE == False:
                    coords.pan_in_coords(Vec2d(-1,0))
                
                # Pan Right
                if event.key == pygame.K_RIGHT and PAUSE == False:
                    coords.pan_in_coords(Vec2d(1,0))
                
                # Pan Up
                if event.key == pygame.K_UP and PAUSE == False:
                    coords.pan_in_coords(Vec2d(0,1))
                
                # Pan Down
                if event.key == pygame.K_DOWN and PAUSE == False:
                    coords.pan_in_coords(Vec2d(0,-1))              
            
            # Mouse Button Down Inputs
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Assign mouse buttons
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                
                # Mouse left press to draw a particle
                if pressed1 == 1 and event.button == 1:
                    
                    # Get the mouse position
                    (posx, posy) = pygame.mouse.get_pos()
                    
                    # The particle is centered at the position the user clicked on
                    particle_center = Vec2d(posx,posy)
                    
                    # The game is paused
                    PAUSE = True
                    
                    # Create a rotatingParticle object and then append to the Particles array
                    particles.append(rotatingParticle(Vec2d(posx,posy), Vec2d(0,0), 1, 0.25, random_bright_color(), coords, BLACK))
                    
                    # The velocity line can be drawn
                    DRAW = True
                
                # Mouse scroll wheel up to increase the particle
                elif event.button == 4 and PAUSE == True:
                    # Enlarge the size up to a maximum radius limit of 3
                    if(particles[count].radius <= 3.0):
                        particles[count].radius += 0.05
                        particles[count].update_radius()
                
                # Mouse scroll wheel down to decrease the particle size
                elif event.button == 5 and PAUSE == True:
                    # Minimize down to a minimum radius radius limit of 0.1
                    if(particles[count].radius >= 0.1):
                        particles[count].radius -= 0.05
                        particles[count].update_radius()
            
            # Mouse Button Up Inputs
            if event.type == pygame.MOUSEBUTTONUP:
                
                # Get the mouse position
                (posx, posy) = pygame.mouse.get_pos()
                
                # Assign mouse buttons
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                
                # Mouse left unpress to unpause
                if pressed1 == 0 and PAUSE == True:
                    DRAW = False
                    PAUSE = False
                    
                    # Increment the particle number in the Particles array
                    count += 1

# Draw a particle's velocity line
def velLine():
    global screen
    
    # Default velocity line value
    velVec = Vec2d(0,0)
    
    # Get mouse position
    (posx, posy) = pygame.mouse.get_pos()
    
    # Draw the line from the circle to the mouse
    pygame.draw.line(screen, RED, particle_center, Vec2d(posx,posy), 1)
    
    # Calculate the velocity using the distance between the particle center and endpoint   
    velVec.x = posx - particle_center.x
    velVec.y = particle_center.y - posy
    
    return velVec

# Detect collisions and then calculate and apply impulses on each particle
def check_particle_collision(obj1, obj2):
    
    # The radius of Particle A
    r1 = obj1.radius
    
    # The radius of Particle B
    r2 = obj2.radius
    
    # Sum of their radius
    both = r1 + r2
    
    # Difference of their velocities
    vel_diff = obj2.vel - obj1.vel
    
    # Distance between the center of the particles
    rVec = obj2.pos - obj1.pos
    
    # Magnitude of the distance between the particles
    rMag = rVec.get_length()
    
    # Absolute x-position of the distance between the particles
    abs_dx = abs((obj2.pos.x - obj1.pos.x))
    
    # Absolute y-position of the distance between the particles
    abs_dy = abs((obj2.pos.y - obj1.pos.y))
    
     # Particles are touching
    if (abs_dx*abs_dx + abs_dy*abs_dy) <= (both*both):
        
        # Elasticty / Coefficient of Restitution
        e = 0
        
        # Reduced mass
        u = (obj1.mass * obj2.mass) / (obj1.mass + obj2.mass)
        
        # Normal unit vector
        n_hat = obj2.pos - obj1.pos
        n_hat = n_hat.normalized()
        
        # Initial normal impulse
        J_normal = Vec2d(0,0)
        
        # Initial perpendicular impulse
        J_perp = Vec2d(0,0)
        
        # Initial tangential (friction) impulse
        J_friction = Vec2d(0,0)
        
        # Distance of the overlap between the circles
        d = both - rMag
        
        # Angular momentum
        L = u * rVec.cross(vel_diff)
        
        # Update the perpendicular impulse
        J_perp = (-d / (rMag * (rMag + d))) * L
        
        # Preventing overlapping by displacing the objects apart
        obj1.pos = obj1.pos - ((u/obj1.mass) * d * n_hat)
        obj2.pos = obj2.pos + ((u/obj2.mass) * d * n_hat)
        
        # Updating momentum
        obj1.mom -= J_perp
        obj2.mom += J_perp
        
        # Updating the velocities
        obj1.update_vel()
        obj2.update_vel()
        
        # Calculate the normal impulse
        if((obj2.vel-obj1.vel).dot(n_hat) > 0):
            pass
        else:
            J_normal = ((1+e) * u * (obj2.vel-obj1.vel).dot(n_hat)) * n_hat
        
        # Coefficient of friction
        uf = 0.01
        
        # Tangential unit vector
        t_hat = n_hat.perpendicular()
        
        # Reduced mass for particle-particle collision and moment of inertia
        u_friction = 1 / (1 / obj1.mass + (obj1.radius * obj1.radius) / obj1.moment + 1 / obj2.mass + (obj2.radius * obj2.radius) / obj2.moment)
        
        # Tangential velocity
        v_friction = (obj2.vel - obj1.vel).dot(t_hat) - obj2.radius * obj2.angvel - obj1.radius * obj1.angvel
        
        # Tangential impulse
        J_friction = -u_friction * v_friction
        
        # Decrease the tangential impulse so it equalizes with the normal impulse
        if abs(J_friction) > uf * J_normal.mag():
           J_friction *=  (uf * abs(J_normal) / abs(J_friction))
        
        # Update the total impulse (normal + tangential) on particle
        J_total = J_normal + J_friction
        
        # Distance from the cenetr of the particle straight to the outside edge
        distance = obj1.pos - obj1.radius * n_hat
        
        # Update the impulse/rotation on collision
        obj1.impulse(J_total, distance)
        obj2.impulse(-J_total, distance)

def check_wall_collision(obj1, obj2):
    
    # Variables that will help keep track of which object is the particle and which is the wall
    objParticle = 0
    objWall = 0
    
    if obj1.type == "wall":
        objWall = obj1
        objParticle = obj2
    else:
        objWall = obj2
        objParticle = obj1

    # Normal unit vector of the wall
    n_hat = objWall.normal
  
    # Distance between the center of the particle and the wall
    distance = (objParticle.pos - objWall.pos).dot(n_hat)
    
    # Distance between the outside of the particle and the wall
    d = objParticle.radius - distance
    
    # Elasticty / Coefficient of Restitution
    e = 0.5
    
    # Initial normal impulse
    J_normal = Vec2d(0,0)

    # The particle is touching the wall
    if (objParticle.radius > distance):
        
        # Calculating the impulse of the bounce
        J_normal = (-(1+e) * objParticle.mass * (objParticle.vel).dot(n_hat)) * n_hat
        
        # Coefficient of friction
        u = 0.5
        
        # Tangential unit vector
        t_hat = n_hat.perpendicular()
        
        # Initial tangential (friction) impulse
        J_friction = Vec2d(0,0)
        
        # Tangential velocity 
        v_friction = (objParticle.vel).dot(t_hat) - objParticle.radius * objParticle.angvel
        
        # Update friction moment of inertia for spinning
        mass_friction = 1 / ((1 / objParticle.mass) + (objParticle.radius * objParticle.radius / objParticle.moment))

        # Friction impulse to be applied
        J_friction = -mass_friction * v_friction * t_hat
        
        # Maximum friction
        max_friction = u * J_normal
        
        # Decrease the tangential impulse so it equalizes with the normal impulse
        if J_friction.mag() > max_friction.mag():
            J_friction *= (u * J_normal.mag()) / J_friction.mag()
        
        # Depenetration
        objParticle.pos = objParticle.pos + (d * n_hat)
        
        # Update the total impulse (normal + tangential) on particle
        J_total = J_normal + J_friction
        
        # Update the impulse/rotation on collision
        objParticle.impulse(J_total, objParticle.pos - objParticle.radius * n_hat)
    else:
        pass

# Calculate and apply forces on each particle
def gravity_force(obj1, obj2):
    
    # The distance between the particles
    rVec = obj1.pos - obj2.pos
    
    # The radius of Particle A
    r1 = obj1.radius
    
    # The radius of Particle B
    r2 = obj2.radius
    
    # Sum of their radius
    both = r1 + r2
    
    # Absolute x-position of the distance between the particles
    abs_dx = abs((obj2.pos.x - obj1.pos.x))
    
    # Absolute y-position of the distance between the particles
    abs_dy = abs((obj2.pos.y - obj1.pos.y))
    
    # If the particles are NOT touching each other then don't apply any force
    if (abs_dx*abs_dx + abs_dy*abs_dy) > (both*both):
        pass
    # Else apply a spring force to the particles to keep them stable
    else:
        # Repulsive force
        force = -15 * (rVec / both)
        
        # Add/Subtract the force to the appropriate particles
        obj1.force += force
        obj2.force -= force
     
    return

# Applies a constant gravity force to each particle
def gravity(obj):
    force = -gravityConstant * obj.mass * Vec2d(0,1)
    obj.force += force

# Main Function
def main():
    global screen, particles, RUNNING, PAUSE, DRAW, count
    
    # Initalize pygame
    pygame.init()
    
    # Set the screen's dimensions
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode([screen_width,screen_height])

    # Set the screen's center
    screen_center = Vec2d(screen_width/2, screen_height/2)
    
    # Set the coordinate system
    # Center of window is (0,0), scale is 1:1, and +y is up
    coords = Coords(screen_center.copy(), 1, True)

    # Zoom in so the scale is 50 pixels per unit
    coords.zoom_at_coords(Vec2d(0,0), 50)
    
    # -------- Main Program Loop -----------\
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Frame rate per second
    frame_rate = 60
    
    # Run at reat time speed
    playback_speed = 1
    
    # Frame rate
    dt = playback_speed/frame_rate
    
    # Set the text font
    basic_font = pygame.font.Font('freesansbold.ttf', 24)
    
    # Pause text
    pause_surf = basic_font.render('Pause (Space)', True, BLACK)
    pause_rect = pause_surf.get_rect()
    pause_rect.center = ((screen_width -120), (screen_height - 50))
    
    # Unpause text
    unpause_surf = basic_font.render('Unpause (Space)', True, BLACK)
    unpause_rect = unpause_surf.get_rect()
    unpause_rect.center = ((screen_width -120), (screen_height - 50))
    
    # Zoom text
    zoom_surf = basic_font.render('Zoom In (-/+)', True, BLACK)
    zoom_rect = zoom_surf.get_rect()
    zoom_rect.center = ((screen_width -120), (screen_height - 150))
    
    # Pan text
    pan_surf = basic_font.render('Pan (Arrow Keys)', True, BLACK)
    pan_rect = pan_surf.get_rect()
    pan_rect.center = ((screen_width -120), (screen_height - 100))
    
    # COM text
    com_surf = basic_font.render('Center of Mass (0)', True, BLACK)
    com_rect = com_surf.get_rect()
    com_rect.center = ((125), (screen_height - 50))
    
    # Scroll Up text
    scrollUp_surf = basic_font.render('Increase Mass (Scroll Up)', True, BLACK)
    scrollUp_rect = scrollUp_surf.get_rect()
    scrollUp_rect.center = ((200), (screen_height - 100))
    
    # Scroll Down text
    scrollDown_surf = basic_font.render('Decrease Mass (Scroll Down)', True, BLACK)
    scrollDown_rect = scrollDown_surf.get_rect()
    scrollDown_rect.center = ((200), (screen_height - 50))
    
    # Running state
    RUNNING = True
    
    # Paused state
    PAUSE = False
    DRAW = False
    
    # Array to keep track of particles
    particles = []
    particles.append(Wall(Vec2d(0, 0), Vec2d(1,3), BLACK, mass=1e99, vel=Vec2d(0,0)))
    particles.append(Wall(Vec2d(0, 0), Vec2d(-3,1), BLACK, mass=1e99, vel=Vec2d(0,0)))
    
    # Particle count
    count = len(particles)
    
    # --- Main Event Loop ---\
    while RUNNING:
        # Check Mouse/Keyboard Input
        getInput(coords)
        
        # --- Paused Game Check---\
        if PAUSE == True:
            
            # Refill the background
            screen.fill(WHITE)
            
            # If the game is paused, draw the velocity line
            if DRAW:
                # Set the particle's velocity to a certain value based on the line drawn
                for particle in particles:
                    if particle.type == "particle":
                        particles[count].set_velocity(velLine() / 12.5)
            
            # Redraw every particle including the new one
            for particle in particles:
                particle.draw(screen, coords)
            
            # Draw unpause text
            screen.blit(unpause_surf, unpause_rect)
            screen.blit(scrollUp_surf, scrollUp_rect)
            screen.blit(scrollDown_surf, scrollDown_rect)
            
            # Update the program with everything drawn
            pygame.display.update()
            
            # This limits the loop to 60 frames per second
            clock.tick(frame_rate)
        
        # --- Unpaused Game Check---\
        elif PAUSE == False:

            # --- Physics ---\
            for i1, particle1 in enumerate(particles):
                for i2, particle2 in enumerate(particles):
                    if i1 < i2:
                        # Check whether the collision is particle-particle or particle-wall/wall-particle
                        if particle1.type == "wall" and particle2.type == "wall":
                            pass
                        elif particle1.type == "wall" or particle2.type == "wall" and particle1.type != particle2.type:
                            check_wall_collision(particle1, particle2)
                        else:
                            check_particle_collision(particle1, particle2)
            
            # Calculate the force on each particle
            for particle in particles:
                particle.force.zero()
                if particle.type == "particle":
                    gravity(particle)

            # Update every particle's physics
            for particle in particles:
                particle.update(dt)
                if particle.type == "particle":
                    particle.update_mom(dt)
                    particle.update_vel()
                    particle.update_angvel()
                    particle.update_angle(dt)
            
            # Change the collision on each particle
            for particle in particles:
                particle.force.zero()

            # --- Drawing ---\
            # Refill the background
            screen.fill(WHITE)
            
            # Redraw every particle
            for particle in particles:
                particle.draw(screen, coords)
            
            # Draw controls text
            screen.blit(pause_surf, pause_rect)
            screen.blit(zoom_surf, zoom_rect)
            screen.blit(pan_surf, pan_rect)
            screen.blit(com_surf, com_rect)
            
            # --- Updates ---\
            # Update the program with everything drawn
            pygame.display.update()
        
            # This limits the loop to 60 frames per second
            clock.tick(frame_rate)

    # Quit the game
    pygame.quit()

# Check if main function exists, else quit the game
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e