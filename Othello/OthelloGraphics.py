 # -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: William Yang
"""

import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
GRASS    = ( 20, 200, 0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 50, 50, 50)
TAN      = ( 210, 180, 140)
OFFWHITE = (235,235,235)
OFFBLACK = (40,40,40)

grid = []
validMoves = []
gameMessage = ""
newTurn = True
gameOver = False
numberPassed = 0
player = "Black"

class Pair:
    def __init__(self, pX, pY):
        self.x = pX
        self.y = pY

def main():
    pygame.init()
    font = pygame.font.SysFont('Calibri', 25, True, False)
 
    #Create window
    width = 255
    height = 255
    screen = pygame.display.set_mode([width,height])
    pygame.display.set_caption('OTHELLO')
    background_color = GRAY

    #Create board
    for row in range(8):
        grid.append([])
        for column in range(8):
            grid[row].append(" ")

    grid[3][3] = "B"
    grid[3][4] = "W"
    grid[4][3] = "W"
    grid[4][4] = "B"
    
    wood = pygame.image.load("wood.jpg")
    wood = pygame.transform.scale(wood, (255, 255))
    boardOffset = 25
    
    #Create Mouse
    pygame.mouse.set_visible(False)
    cursor = pygame.image.load("hand.png")
    cursor = pygame.transform.scale(cursor, (20, 20))
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------\
    global numberPassed
    global player
    global validMoves
    global newTurn 
    global gameOver
    
    whiteScore = 0
    blackScore = 0
    done = False

    while not done:
        """Check for forfeiting turns"""
        if (player == "White" and checkAvailableMoves("W", "B") == 0 and newTurn and not gameOver):
            print("White Turn Forfeited")
            updateGameMessage("White Turn Forfeited")
            player = "Black"
            numberPassed += 1
            newTurn = True
        elif player == "White":
            newTurn = False
        
        if (player == "Black" and checkAvailableMoves("B", "W") == 0 and newTurn and not gameOver):
            print("Black Turn Forfeited")
            updateGameMessage("Black Turn Forfeited")
            player = "White"
            numberPassed += 1
            newTurn = True
        elif player == "Black":
            newTurn = False
            
        """Check for game over"""
        if numberPassed >= 2 and not gameOver:
            print("\nGame Over")
            print("")
            gameOver = True
                        
            if blackScore > whiteScore:
                print("\033[4m\nBlack Wins!\n\033[0m")
                updateGameMessage("Black Wins!")
            elif whiteScore > blackScore:
                print("\033[4m\nWhite Wins!\n\033[0m")
                updateGameMessage("White Wins!")
            else:
                print("\033[4m\nTie\033[0m")
                updateGameMessage("Tie!")
        
        # --- Main event loop
        """ Event Handling """
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            elif event.type == pygame.KEYDOWN:
                #print(event.key, event.mod, event.unicode)
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed.")
            # Player clicks a square
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                pos = pygame.mouse.get_pos()
                column = (pos[1] - boardOffset) // 25
                row = (pos[0] - boardOffset )// 25
                if row < 8 and column < 8:
                    if player == "White":
                        if checkPoint(row, column, "W", "B"):
                            numberPassed = 0
                            player = "Black"
                            addToGrid(row, column, "W")
                            validMoves = []
                            newTurn = True
                    else:
                        if checkPoint(row, column, "B", "W"):
                            numberPassed = 0
                            player = "White"
                            addToGrid(row, column, "B")
                            validMoves = []
                            newTurn = True
                    
                    print("You have clicked the square:",row + 1,",",column + 1)
                    
                    # Update score
                    whiteScore = 0
                    blackScore = 0
                    for x in range(0, 8):
                        for y in range(0, 8):
                            if getFromGrid(x, y) == "W":
                                whiteScore += 1
                            elif getFromGrid(x, y) == "B":
                                blackScore += 1
        
        """ State Checking """
        currentPos = pygame.mouse.get_pos()
        currentColumn = (currentPos[1] - boardOffset) // 25
        currentRow = (currentPos[0] - boardOffset ) // 25
        for i in validMoves:
            if i.x == currentRow and i.y == currentColumn:
                if player == "White":
                    addToGrid(currentRow, currentColumn, "HW")
                else:
                    addToGrid(currentRow, currentColumn, "HB")
            else:
                addToGrid(i.x, i.y, " ")
        
        """Drawing to screen"""
        # Background
        screen.blit(wood, [0,0])
        pygame.draw.rect(screen, background_color, [26,26,205,205]) 
        
        # Score board
        pygame.draw.circle(screen, WHITE, [65, 15], 10)
        pygame.draw.circle(screen, OFFWHITE, [165, 15], 8)
        text = font.render(str(whiteScore),True, WHITE)
        screen.blit(text, [80,5])
        
        pygame.draw.circle(screen, BLACK, [165, 15], 10)
        pygame.draw.circle(screen, OFFBLACK, [165, 15], 8)
        text = font.render(str(blackScore),True, WHITE)
        screen.blit(text, [180,5])
        
        # Game Messages
        text = font.render(str(gameMessage),True, WHITE)
        screen.blit(text, [0,235])
        
        #  Game Board and Pieces
        for row in range(8):
            for column in range(8):
                color = GRASS
                color2 = GRASS
                if grid[row][column] == "W":
                    color = WHITE
                    color2 = OFFWHITE
                elif grid[row][column] == "B":
                    color = BLACK
                    color2 = OFFBLACK
                elif grid[row][column] == "HW":
                    color = WHITE
                    color2 = GRASS
                elif grid[row][column] == "HB":
                    color = BLACK
                    color2 = GRASS
                pygame.draw.rect(screen, GRASS, [(5+20) * column + boardOffset + 5, 
                                               (5+20) * row + boardOffset + 5,
                                               22, 22])
                pygame.draw.circle(screen, color, [(5+10) * column + (10 * column) + boardOffset + 16,
                                                   (5+10) * row + (10 * row) + boardOffset + 16]
                                                    ,10)
                pygame.draw.circle(screen, color2, [(5+10) * column + (10 * column) + boardOffset + 16,
                                                   (5+10) * row + (10 * row) + boardOffset + 16]
                                                    ,8)
        
        # Held Piece and Cursor
        if player == "White":
            pygame.draw.circle(screen, WHITE, [currentPos[0], currentPos[1]], 10)
            pygame.draw.circle(screen, OFFWHITE, [currentPos[0], currentPos[1]], 8)
        else:
            pygame.draw.circle(screen, BLACK, [currentPos[0], currentPos[1]], 10)
            pygame.draw.circle(screen, OFFBLACK, [currentPos[0], currentPos[1]], 8)
            
        screen.blit(cursor, [currentPos[0], currentPos[1]])
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        clock.tick(60)
    
    pygame.quit()

def getFromGrid(rows, columns):
    return grid[columns][rows]

def addToGrid(x, y, icon):
    grid[y][x] = icon
    
def updateGameMessage(message):
    global gameMessage
    gameMessage = message
    
def checkAvailableMoves(icon, opponentIcon):
    global validMoves
    validMoves = []
    possibleMoves = 0

    # Loop through entire grid
    for x in range(0, 8):
        for y in range(0, 8):
            validMove = False
            
            if getFromGrid(x, y) == " " or getFromGrid(x, y) == "HW" or getFromGrid(x, y) == "HB":
    
                # Check for Flipping
                
                # Check to the Right
                FlipList = []
                for i in range(1, 8 - x):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y) == opponentIcon:
                        FlipList.append(Pair(x + i, y))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y) == icon:
                        # Check valid move        
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
            
                # Check to the Left
                FlipList = []
                for i in range(1, x + 1):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y) == opponentIcon:
                        FlipList.append(Pair(x - 1, y))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
         
                # Check Down
                FlipList = []
                for i in range(1, 8 - y):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, y + i) == opponentIcon:
                        FlipList.append(Pair(x, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
                
                # Check Up
                FlipList = []
                for i in range(1, y + 1):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, y - i) == opponentIcon:
                        FlipList.append(Pair(x, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
   
                # Check Up-Right             
                FlipList = []

                distY = y + 1
                distX = 8 - x
                minimumDistance = 0
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y - i) == opponentIcon:
                        FlipList.append(Pair(x + i, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break

                # Check Up-Left               
                FlipList = []

                distY = y + 1
                distX = x + 1
        
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y - i) == opponentIcon:
                        FlipList.append(Pair(x - i, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
  
                # Check Down-Left              
                FlipList = []

                distY = 8 - y
                distX = x + 1
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y + i) == opponentIcon:
                        FlipList.append(Pair(x - i, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
    
                # Down-Right            
                FlipList = []
                    
                distY = 8 - y
                distX = 8 - x
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y + i) == opponentIcon:
                        FlipList.append(Pair(x + i, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
                
                FlipList = []
                
                if validMove:
                    validMoves.append(Pair(x, y))
                    possibleMoves += 1
    
    return possibleMoves

def checkPoint(x, y, icon, opponentIcon):
    # print("X: " + str(x) + "Y: " + str(y))
    
    validMove = False
    
    if getFromGrid(x, y) == " " or getFromGrid(x, y) == "HW" or getFromGrid(x, y) == "HB":

        # Check for Flipping
        
        # Check to the right
        FlipList = []
        for i in range(1, 8 - x):
            # If the tile has your opponent's icon
            if getFromGrid(x + i, y) == opponentIcon:
                FlipList.append(Pair(x + i, y))
                # print(str(i)+", "+str(x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y) == icon:
                # print(str(x)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    # Grid[j.x][j.y] = icon
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i)+", "+str(x)+" is blank")
                break
        
        # List of disks to be flipped
        FlipList = []
        # Check to the left
        for i in range(1, x + 1):
            # If the tile has your opponent's icon
            if getFromGrid(x - i, y) == opponentIcon:
                FlipList.append(Pair(x - i, y))
                # print(str(i)+", "+str(x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y) == icon:
                # print(str(x)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    # Grid[j.x][j.y] = icon
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i)+", "+str(x)+" is blank")
                break
        
        FlipList = []
        # Check Down
        for i in range(1, 8 - y):
            # If the tile has your opponent's icon
            if getFromGrid(x, y + i) == opponentIcon:
                FlipList.append(Pair(x, y + i))
                # print(str(y)+", "+str(i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x, y + i) == icon:
                # print(str(y)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y)+", "+str(i)+" is blank")
                break
            
        FlipList = []
        # Check Up
        for i in range(1, y + 1):
            # If the tile has your opponent's icon
            if getFromGrid(x, y - i) == opponentIcon:
                FlipList.append(Pair(x, y - i))
                # print(str(y)+", "+str(i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x, y - i) == icon:
                # print(str(y)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y)+", "+str(i)+" is blank")
                break
        
        FlipList = []
        
        # Check Down-Right
        
        distY = 8-y
        distX = 8-x
        
        minimumDistance = 0
        
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x + i, y + i) == opponentIcon:
                FlipList.append(Pair(x + i, y + i))
                # print(str(i + y)+", "+str(i + x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y + i) == icon:
                # print(str(i + y)+", "+str(i + x)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i + y)+", "+str(i + x)+" is blank")
                break
        
        FlipList = []
        
        
        # Up-right
        distY = y + 1
        distX = 8 - x
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x + i, y - i) == opponentIcon:
                FlipList.append(Pair(x + i, y - i))
                # print(str(i + y)+", "+str(x - i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y - i) == icon:
                # print(str(i + y)+", "+str(x - i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i + y)+", "+str(x - i)+" is blank")
                break
        
        FlipList = []
        
        # Up-Left
        distY = y + 1
        distX = x + 1
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x - i, y - i) == opponentIcon:
                FlipList.append(Pair(x - i, y - i))
                # print(str(y - i)+", "+str(x - i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y - i) == icon:
                # print(str(y - i)+", "+str(x - i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y - i)+", "+str(x - i)+" is blank")
                break
        
        FlipList = []
            
        
        # Down-left
        distY = 8 - y
        distX = x + 1
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x - i, y + i) == opponentIcon:
                FlipList.append(Pair(x - i, y + i))
                # print(str(y - i)+", "+str(x + i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y + i) == icon:
                # print(str(y - i)+", "+str(x + i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y - i)+", "+str(x + i)+" is blank")
                break
        
        FlipList = []
    else:
        print("Occupied Space")
        updateGameMessage("Occupied Space")
        return False
    #Break out of the loop if the input is valid
    if validMove:
        updateGameMessage("")
        return True
    else:
        print("\033[4m\nInvalid Move\033[0m")
        updateGameMessage("Invalid Move")
        print("Possible Moves: ", checkAvailableMoves(icon, opponentIcon))
        return False
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise


