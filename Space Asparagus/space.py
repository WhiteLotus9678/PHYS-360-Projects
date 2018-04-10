# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:16:50 2018

@author: Will Yang, Alec Maki, Drew Brey
"""

import pygame

# Utility purposes
from vec2d import Vec2d
from coords import Coords

# Objects
from background import Background
from player import Player
from meteor import Meteor
from planet import Planet
from asparagus import Asparagus

# Initalize color(s)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

""" Exit Game """
def terminate():
    pygame.quit()
    
def introMode(font):
    basic_font = font
    intro = True
    
    title_surf = basic_font.render('SPACE ASPARAGUY', True, WHITE)
    title_rect = title_surf.get_rect()
    title_rect.center = (screen_width / 2, (screen_height / 2) - 90)
    
    intro_surf = basic_font.render('Press Space to start', True, WHITE)
    intro_rect = intro_surf.get_rect()
    intro_rect.center = (screen_width / 2, (screen_height / 2) - 0)
    
    intro_surf2 = basic_font.render('Use WASD keys to move.', True, WHITE)
    intro_rect2 = intro_surf2.get_rect()
    intro_rect2.center = (screen_width / 2, (screen_height / 2) + 60)
    
    while(intro):
        screen.blit(title_surf, title_rect)
        screen.blit(intro_surf, intro_rect)
        screen.blit(intro_surf2, intro_rect2)
        
        pygame.display.update()
        
        # Enter into the game
        KEY = pygame.key.get_pressed()        
        if KEY[pygame.K_SPACE] and intro:
            intro = False
        
        CLICK = pygame.mouse.get_pressed()
        if CLICK[0] and intro:
            intro = False
        
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

"""Spawn Meteors"""
def spawn_meteors(num):
    for i in range(num):        
        # This represents a meteor
        meteor = Meteor(Vec2d(0,0), 1,  0.4)

        # Set a random location for the meteors
        meteor.reset_pos(screen_width)

        # Add the meteor to the list of objects
        meteor_list.add(meteor)
        all_sprites_list.add(meteor)

"""Spawn Asparagi"""
def spawn_asparagi(num):
    for i in range(num):
        # This represents an asparagus
        asparagus = Asparagus(Vec2d(0,0), 1, "SpaceAssets/Asparagus.png", 0.08)
        
        # Set a random location for the asparagus
        asparagus.reset_pos(screen_width)
        
        # Add the asparagus to the list of objects
        asparagus_list.add(asparagus)
        all_sprites_list.add(asparagus)

"""Spawn Planets"""
def spawn_planets(num):
    global planet
    for i in range(num):
        # This represents a planet
        planet = Planet(Vec2d(1,1), 50, 0.5)
        
        # Set a random location for the planets
        planet.reset_pos(screen_width)
        
        # Add the planet to the list of objects
        planet_list.add(planet)
        all_sprites_list.add(planet)

"""State Checking for Player Movement"""
def get_key(KEY):
    # Up Movement
    if KEY[pygame.K_UP] or KEY[pygame.K_w]:
        player.force += Vec2d(0, -1000)
    
    # Down Movement
    if KEY[pygame.K_DOWN] or KEY[pygame.K_s]:
        player.force += Vec2d(0, 2000)
    
    # Left Movement
    if KEY[pygame.K_LEFT] or KEY[pygame.K_a]:
        player.force += Vec2d(-1000, 0)
    
    # Right Movement
    if KEY[pygame.K_RIGHT] or KEY[pygame.K_d]:
        player.force += Vec2d(1000, 0)

"""Draw Objects"""
def update_objects():
    player.update(dt, coords, 0.125)
    planet_list.update(dt, screen_width, screen_height)
    asparagus_list.update(dt, screen_width, screen_height)
    meteor_list.update(dt, screen_width, screen_height)

"""Screen Boundaries"""
def check_bounds():
    # Prevent the player from moving past the upper and lower boundaries of the screen
    # Going past the screen to the left or right moves the player to the
    # opposite side of the screen
    if player.pos.x <= 0:
        player.pos.x = screen_width - 15
    elif player.pos.x >= screen_width - 15:
        player.pos.x = 0
    elif player.pos.y <= 0:
        player.force += Vec2d(0, 3000)
    elif player.pos.y >= screen_height - 100:
        player.force += Vec2d(0, -3000)

"""Score Points"""
def set_score():
    global score, screen
    # See if the player has collided with any asparagi
    asparagi_hit_list = pygame.sprite.spritecollide(player, asparagus_list, False)
    
    # Check the list of collisions with asparagi and then reset the game
    for asparagi in asparagi_hit_list:
        score += 1
        print("Score: ", score)
        
        # Reset asparagus to the top of the screen to fall again.
        asparagi.reset_pos(screen_width)  

""" Lose the Game """
def check_lose():
    global score
    # See if the player has collided with any meteors.
    meteors_hit_list = pygame.sprite.spritecollide(player, meteor_list, False)
    
    # Check the list of collisions with meteors and then reset the game
    for meteors in meteors_hit_list:
        score = 0
        player.reset_pos(coords)
        
        for meteor in meteor_list:
            # Reset meteor to the top of the screen to fall again.
            meteor.reset_pos(screen_width)
            
        for planet in planet_list:
            # Reset planet to the top of the screen to fall again.
            planet.reset_pos(screen_width)
        
        for asparagus in asparagus_list:
            # Reset asparagus to the top of the screen to fall again.
            asparagus.reset_pos(screen_width)

    
    # See if the player has collided with any planets.
    planets_hit_list = pygame.sprite.spritecollide(player, planet_list, False) 
    
    # Check the list of collisions with planets and then reset the game
    for planets in planets_hit_list:
        score = 0
        player.reset_pos(coords)
        
        for meteor in meteor_list:
            # Reset meteor to the top of the screen to fall again.
            meteor.reset_pos(screen_width)
        
        for planet in planet_list:
            # Reset planet to the top of the screen to fall again.
            planet.reset_pos(screen_width)
        
        for asparagus in asparagus_list:
            # Reset planet to the top of the screen to fall again.
            asparagus.reset_pos(screen_width)

""" Main Function """
def main():
    global player, planet, screen_width, meteor_list, asparagus_list, planet_list, all_sprites_list, meteor_hit_list, planet_hit_list
    global score, dt, coords, screen_width, screen_height, screen
    
    # Initialize Pygame
    pygame.init()
    
    # Set the height and width of the screen    
    screen_width = 1200
    screen_height = 800
    
    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Set the center of the screen for coordinates
    screen_center = Vec2d(0,0)
    coords = Coords(screen_center, 1, False)
    # ^ Center of window is (0,0), scale is 1:1, and +y is up
    
    # Text font
    basic_font = pygame.font.Font('freesansbold.ttf', 36)

    # Set the background
    backGround = Background('SpaceAssets/background_image.png', [0,0])
    
    # Title Screen
    introMode(basic_font)
    
    # Selects and plays music
    pygame.mixer.music.load('SpaceAssets/SpaceTheme.mp3')
    pygame.mixer.music.play(0)
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Loop until the user quits the program
    done = False
    
    # This is a list of 'sprites.' Each meteor in the program is
    # added to this list. The list is managed by a class called 'Group.'
    meteor_list = pygame.sprite.Group()
    
    # Each asparagus in the program is added to this list.
    asparagus_list = pygame.sprite.Group()
    
    # Each planet in the program is added to this list.
    planet_list = pygame.sprite.Group()
    
    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()
    
    #Spawn meteors 
    spawn_meteors(5)

    # Spawn asaparagi
    spawn_asparagi(5)

    # Spawn planets
    spawn_planets(1)
    
    # Spawn the player object and add it to a list of objects
    player = Player(Vec2d(0,0), Vec2d(0,1), 1, screen_width, screen_height, "SpaceAssets/SpaceShip.png", 0.1)
    all_sprites_list.add(player)
    
    # Frames per second
    frame_rate = 30
    
    # 1 is real time, 10 is 10x real speed, etc.
    playback_speed = 1
    
    # Change in time based on FPS and playback speed
    dt = playback_speed/frame_rate
    
    # Air drag coefficient
    c = 2/300
    
    # Gravitational coefficient
    G = 10000000
    
    # Player score
    score = 0
    
    # -------- Main Program Loop -----------
    while not done:
        
        """Event Handler"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        """Force Calculations"""
        # Calculate distance between player and planet        
        rVec = player.pos - planet.pos
        # r = rVec.get_length() # Vector of the distance between the player and planet
        rHat = rVec.normalized() # Unit vector

        # Air resistance
        player.force = -c * player.vel.get_length_sqrd() * player.vel.normalized()
                
        # Pulls the player towards a planet
        if(True):
            player.force += (-G * rHat) / rVec.get_length_sqrd()
        
        """State Checking"""
        # Set player controls
        KEY = pygame.key.get_pressed()        
        get_key(KEY)
        
        """Screen Boundaries"""
        # Check if player touches screen boundaries
        check_bounds()
        
        """Draw objects"""
        # Move all of the sprites according to physics
        update_objects()
        
        """Score Points"""
        # Calculate and print the score
        set_score()
        
        """Lose Condition"""
        # Player loses the game
        check_lose()
        
        """Drawing"""
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw and move the background down
        backGround.update(screen)
        
        # Draw blocks to the screen
        all_sprites_list.draw(screen)
        
        # Score display settings
        score_surf = basic_font.render('Score: {0}'.format(score), True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.center = (100, 50)
        
        # Show the score
        screen.blit(score_surf, score_rect)
        
        pygame.display.update()
        
        # Limit to 20 frames per second
        clock.tick(frame_rate)
    
    # Quit the game
    terminate()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise