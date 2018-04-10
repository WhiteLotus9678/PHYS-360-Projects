# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: William Yang
"""
import pygame

# Define some colors
WHITE    = ( 255, 255, 255)
YELLOW   = ( 255, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)

#checks for if a player has won
def Win(array, cord_array, player_num):
    #set counter variables
    counter = 1
    counter2 = 1
    counter3 = 1
    counter4 = 1
    
    #Check for horizontal Victories
    j = 0
    while True:
        if cord_array[1] - j != 0:
            j += 1
            if array[cord_array[0]][cord_array[1] - j] == player_num:
                counter += 1
            else:
                break
        else:
            break
    j = 0
    while True:
        if cord_array[1] + j != 5:
            j += 1
            if array[cord_array[0]][cord_array[1] + j] == player_num:
                counter += 1
            else:
                break
        else:
            break
        
    #Check for Vertical Victories
    j = 0
    while True:
        if cord_array[0] + j != 6:
            j += 1
            if array[cord_array[0] + j][cord_array[1]] == player_num:
                counter2 += 1
            else:
                break
        else:
            break
    j = 0
    while True:
        if cord_array[0] - j != 0:
            j += 1
            if array[cord_array[0] - j][cord_array[1]] == player_num:
                counter2 += 1
            else:
                break
        else:
            break
        
    #check for diagonal Vicories (from bottom left to top Right)
    j = 0
    while True:
        if cord_array[1] - j != 0:
            if cord_array[0] + j != 6:
                j += 1
                if array[cord_array[0] + j][cord_array[1] - j] == player_num:
                    counter3 += 1
                else:
                    break
            else:
                break
        else:
            break
    j = 0
    while True:
       if cord_array[1] + j != 5:
           if cord_array[0] - j != 0:
               j += 1
               if array[cord_array[0] - j][cord_array[1] + j] == player_num:
                   counter3 += 1
               else:
                   break
           else:
               break
       else:
           break
    
    #Check for diagonal Victories (bottom right to top left)
    j = 0
    while True:
        if cord_array[1] + j != 5:
            if cord_array[0] + j != 6:
                j += 1
                if array[cord_array[0] + j][cord_array[1] + j] == player_num:
                    counter4 += 1
                else:
                    break
            else:
                break
        else:
            break
    j = 0
    while True:
       if cord_array[1] - j != 0:
           if cord_array[0] - j != 0:
               j += 1
               if array[cord_array[0] - j][cord_array[1] - j] == player_num:
                   counter4 += 1
               else:
                   break
           else:
               break
       else:
           break
       
    # Check if any of the counders produced a win
    if counter >= 4:
        return True
    elif counter2 >= 4:
        return True
    elif counter3 >= 4:
        return True
    elif counter4 >= 4:
        return True
    else:
        return False

def main():
    pygame.init()
    font = pygame.font.SysFont('Calibri', 25, True, False)
    '''
    Variables consisting of witch player's turn it is, 
    the cordinates of the players peice
    the array of the game board
    a variable for storing what colomb we are in
    whether or not a win state has been achieved
    and how many turns have passed
    '''
    player_num = 1
    cord_array = [0,0]
    array = []
    n = None
    win = False
    full = False
    counter = 0
    
    for i in range (7):
        array.append([0,0,0,0,0,0])
    
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    
    m_pos = pygame.mouse.get_pos()
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------\
    done = False
    while not done:
        if win == False:
            # --- Main event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # If user clicked close
                    done = True
                #checking on mouse click which column was clicked on
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    m_pos_x = m_pos[0]
                    i = 170
                    j = 1
                    while True:
                        if m_pos_x > i and m_pos_x <= i + 60:
                            n = j
                            break
                        if i == 470:
                            n = None
                            break
                        i += 60
                        j += 1
                    
                    #resets the full colomn variable
                    full = False
                    
                    # Updates the gameboard array with the appropriate piece
                    if n != None:
                        i = 6
                        while True:
                            if array[i][n-1] == 0:
                                array[i][n - 1] = player_num
                                cord_array = [i, n - 1]
                                counter += 1
                                break
                            if i == 0:
                                full = True
                                break
                            i = i - 1
                            
                        #checks for a win, if there is one, dont swap the player, otherwise do
                        win = Win(array, cord_array, player_num)
                        if full == False:
                            if win == False:
                                if player_num == 1:
                                    player_num = 2
                                else:
                                    player_num = 1
            #Checks where the mouse is currently and sets a variable to the appropriate column 
            mouse = pygame.mouse.get_pos()
            i = 170
            j = 0
            while True:
                if mouse[0] > i and mouse[0] <= i + 60:
                    c = j
                    break
                if j == 6:
                    c = 7
                    break
                j += 1
                i += 60
            
            # --- Drawing code should go here
            # First, clear the screen
            background_color = WHITE 
            screen.fill(background_color) 
            # Now, do your drawing.
            pygame.draw.rect(screen, BLUE, (150, 150, 400, 450))
            y = 200
            x = 200
            
            #draws the circles on the board, changing there color according to different peramiters
            for j in range (6):
                y = 200
                for i in range (7):
                    if array[i][j] == 0:
                        if j == c:
                            pygame.draw.circle(screen, GREEN, (x ,y), 25)
                        else:
                            pygame.draw.circle(screen, WHITE, (x ,y), 25)
                    elif array[i][j] == 1:
                        pygame.draw.circle(screen, YELLOW, (x ,y), 25)
                    else:
                        pygame.draw.circle(screen, RED, (x ,y), 25)
                    y += 60
                x += 60
                
            if full == True:
                text = font.render("THAT COLOMN IS FULL! Try another", True, BLUE)
                screen.blit(text, [50,50])
            elif player_num == 1 and win == False:
                text = font.render("Yellow's Turn:", True, YELLOW)
                screen.blit(text, [50,50])
            elif player_num == 2 and win == False:
                text = font.render("Red's Turn:", True, RED)
                screen.blit(text, [50,50])
            if counter == 41:
                win = True
            # --- Update the screen with what we've drawn.
            pygame.display.update()
        
            # This limits the loop to 60 frames per second
            clock.tick(60)
        else:
            #checks if a click has happened since a win has occured, if so, it resets the array and sets win back to false
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # If user clicked close
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range (7):
                        array[i] = [0,0,0,0,0,0]
                    counter = 0
                    win = False
                    
            #Prints who one and how to restart
            if player_num == 1 and counter != 41:
                text = font.render("Yellow Wins! Click to Restart", True, YELLOW)
                screen.blit(text, [50,50])
            elif player_num == 2 and counter != 41:
                text = font.render("Red Wins! Click to Restart", True, RED)
                screen.blit(text, [50,50])
            else:
                text = font.render("Tie! Click to Restart", True, BLUE)
                screen.blit(text, [50,50])
            pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
