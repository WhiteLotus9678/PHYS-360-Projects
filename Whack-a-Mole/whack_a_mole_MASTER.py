# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:33:47 2018

@author: Will Yang, Drew Brey, Alec Maki
"""
import pygame, random

# Colors     R    G    B
GRASS    = (  24, 255,   0) # Color for background
BROWN    = ( 137,  87,  35) # Color for mole
BLUE     = (   0,   0, 255) # Color for text

""" Exit the game """
def terminate():
    pygame.quit()

""" Randomly selects and plays the music """
def selectMusic():
   if RAND_MUSIC == 0:
       pygame.mixer.music.load('Cantata Mortis.mp3')
   else:
       pygame.mixer.music.load('You Say Run.mp3')
   pygame.mixer.music.play(0)

""" Start Screen """
def introMode(intro):
    INTRO_MODE = intro
    
    while INTRO_MODE:
       WINDOW.fill(GRASS)
       WINDOW.blit(INTRO_SURF, INTRO_RECT)
       WINDOW.blit(INTRO_SURF2, INTRO_RECT2)
       WINDOW.blit(INTRO_SURF3, INTRO_RECT3)
       WINDOW.blit(INTRO_SURF4, INTRO_RECT4)
       pygame.display.update()
        
       # State Checking
       KEY = pygame.key.get_pressed()
       if KEY[pygame.K_SPACE] and INTRO_MODE:
           INTRO_MODE = False
       
       CLICK = pygame.mouse.get_pressed()
       if CLICK[0] and INTRO_MODE:
           INTRO_MODE = False
        
       # Event Handler
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               terminate()

""" Resets all drawings on the screen """
def fillGrass():
    WINDOW.fill(GRASS)
    
""" Show the player score """
def showScore():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    
    SCORE_SURF = BASICFONT.render('Score: {0}'.format(SCORE), True, BLUE)
    SCORE_RECT = SCORE_SURF.get_rect()
    SCORE_RECT.center = (100, 105)
    WINDOW.blit(SCORE_SURF, SCORE_RECT)

""" Show the countdown timer """
def showTime(end):
    END = end
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    
    TIME_SURF = BASICFONT.render('Time: {0}'.format(round(END,1)), True, BLUE)
    TIME_RECT = TIME_SURF.get_rect()
    TIME_RECT.center = (110, 45)
    WINDOW.blit(TIME_SURF, TIME_RECT)

""" Win Screen """
def winMode():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)

    if SCORE >= 38:
        WIN_SURF = BASICFONT.render('Holy moley!', True, BLUE)
        WIN_RECT = WIN_SURF.get_rect()
        WIN_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 60)
    elif SCORE >= 18:
        WIN_SURF = BASICFONT.render('The moles have retreated for now...', True, BLUE)
        WIN_RECT = WIN_SURF.get_rect()
        WIN_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 60)
    else:
        WIN_SURF = BASICFONT.render('Better luck next time...', True, BLUE)
        WIN_RECT = WIN_SURF.get_rect()
        WIN_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 60)
    WIN_SURF2 = BASICFONT.render('You whacked ' + str(SCORE) + ' moles !!!', True, BLUE)
    WINDOW.blit(WIN_SURF, WIN_RECT)
    WINDOW.blit(WIN_SURF2, WIN_RECT2)
    WINDOW.blit(WIN_SURF3, WIN_RECT3)

""" Main Function """
def main():

   # Global Variables
   global RAND_MUSIC, HALF_WINWIDTH, HALF_WINHEIGHT, SCORE, INTRO_MODE, WINDOW

   WINWIDTH = 800 # Display width
   WINHEIGHT = 800 # Display height
   HALF_WINWIDTH = int(WINWIDTH / 2)
   HALF_WINHEIGHT = int(WINHEIGHT / 2)
   RATE = 300000 # Rate at which the circles show up, high = slow
   RAND_MUSIC = random.randint(0, 1)
   RAND_X = random.randrange(100, 700) # Random X position for the mole
   RAND_Y = random.randrange(100, 700) # Random Y position for the mole
   SCORE = 0 # Player's score
   RUNNING = True # The game is running
   INTRO_MODE = True # Start screen is ON
   WIN_MODE = False # Win screen is OFF
   WINDOW = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
   MOLE = pygame.draw.circle(WINDOW, BROWN, [400, 400], 50, 0) # Size of the mole
   START_TICKS = 0
   END = 0 # Time the player gets to whack the moles
   TIME_LIMIT = 30 # Time player gets to play
   
   pygame.init()
   
   pygame.display.set_caption('Whack-A-Mole!') # Name of the game
   pygame.display.set_icon(pygame.image.load('gameicon.jpg')) # Program icon
    
   """
   In-game Text
   """
   global GAME_OVER, GAME_OVER_RECT, INTRO_SURF, INTRO_RECT, INTRO_SURF2, INTRO_RECT2, INTRO_SURF3, INTRO_RECT3
   global INTRO_SURF4, INTRO_RECT4, WIN_SURF, WIN_RECT, WIN_SURF2, WIN_RECT2, WIN_SURF3, WIN_RECT3

   BASICFONT = pygame.font.Font('freesansbold.ttf', 36)
    
   # Game Over
   GAME_OVER = BASICFONT.render('Game Over', True, BLUE)
   GAME_OVER_RECT = GAME_OVER.get_rect()
   GAME_OVER_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
    
   # Title Screen
   INTRO_SURF = BASICFONT.render('WHACK-A-MOLE', True, BLUE)
   INTRO_RECT = INTRO_SURF.get_rect()
   INTRO_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 60)
    
   INTRO_SURF2 = BASICFONT.render('Use your mouse to whack as many moles', True, BLUE)
   INTRO_RECT2 = INTRO_SURF2.get_rect()
   INTRO_RECT2.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
    
   INTRO_SURF3 = BASICFONT.render('as you can within the time limit!', True, BLUE)
   INTRO_RECT3 = INTRO_SURF3.get_rect()
   INTRO_RECT3.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)
    
   INTRO_SURF4 = BASICFONT.render('Press SPACE to start!', True, BLUE)
   INTRO_RECT4 = INTRO_SURF4.get_rect()
   INTRO_RECT4.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 90)
   
   # Win Screen
   WIN_SURF = BASICFONT.render('Holy moley!', True, BLUE)
   WIN_RECT = WIN_SURF.get_rect()
   WIN_RECT.center = (HALF_WINWIDTH, HALF_WINHEIGHT - 60)
    
   WIN_SURF2 = BASICFONT.render('You whacked ' + str(SCORE) + ' moles !!!', True, BLUE)
   WIN_RECT2 = WIN_SURF2.get_rect()
   WIN_RECT2.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
    
   WIN_SURF3 = BASICFONT.render('(Press "R" to restart.)', True, BLUE)
   WIN_RECT3 = WIN_SURF3.get_rect()
   WIN_RECT3.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)
    
   selectMusic() 
   introMode(INTRO_MODE)
   fillGrass()
   
   pygame.mouse.set_cursor(*pygame.cursors.broken_x) # Mouse cursor
   START_TICKS = pygame.time.get_ticks()
   
   while RUNNING:
       if RATE == 300000 and not WIN_MODE:
           fillGrass()
           
           # Randomly draw a  mole
           RAND_X = random.randrange(100, 700)
           RAND_Y = random.randrange(100, 700)
           MOLE = pygame.draw.circle(WINDOW, BROWN, [RAND_X, RAND_Y], 50, 0)
    
           # Show the player score as in-game text 
           showScore()
    
           # Counts down the timer and then output it as text
           END = TIME_LIMIT - (pygame.time.get_ticks() - START_TICKS) / 1000 # Calculate how many seconds
           showTime(END)
           
           # Reset the rate
           RATE = 0
           
           pygame.display.update()

       if END < 0:
           fillGrass()
           END = 0.0
           showScore()
           showTime(END)
           pygame.display.update()
           WIN_MODE = True
        
       if WIN_MODE:
           winMode()
           pygame.display.update()
        
       RATE = RATE + 1
    
       # Event Handler
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               RUNNING = False
                
           if event.type == pygame.MOUSEBUTTONDOWN:
               pos = pygame.mouse.get_pos()
               (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
               if MOLE.collidepoint(pos) & pressed1 == 1 and not WIN_MODE:
                   SCORE = SCORE + 1
                   RATE = 300000
            
           elif event.type == pygame.KEYDOWN:
               if WIN_MODE and event.key == pygame.K_r:
                   SCORE = 0
                   RATE = 300000
                   END = 0
                   START_TICKS = pygame.time.get_ticks()
                   WINDOW.fill(GRASS)
                   WIN_MODE = False
    
   terminate()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise