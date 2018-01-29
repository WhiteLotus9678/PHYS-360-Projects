# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 15:10:09 2018

@title: Tic-Tac-Toe
@author: Student
"""

def check_players():
    draw_board('1', '2', '3', '4', '5', '6', '7', '8', '9')
    playerOne = input("Is player 1 ready? (Y/N)\n")
    playerTwo = input("Is player 2 ready? (Y/N)\n")
    
    if ((playerOne == 'Y') and (playerTwo == 'Y')):
        return True
    else:
        return False

def play():
    # print("Play test confirmed.")
    a11 = '1'
    a12 = '2'
    a13 = '3'
    a21 = '4'
    a22 = '5'
    a23 = '6'
    a31 = '7'
    a32 = '8'
    a33 = '9'
    
    while True:
        print("\n")
        draw_board(a11, a12, a13, a21, a22, a23, a31, a32, a33)
        decisionOne = input("Player 1, choose a space (1-9):\n")
        decisionTwo = input("Player 2, choose a space (1-9):\n")
        break
    
    return 0

def draw_board(a11, a12, a13, a21, a22, a23, a31, a32, a33):
    n = 0
    if (a11 == ''):
        n = 1
    # print(n, board)
    print("-------------")
    print("|", a11, "|", a12, "|", a13, "|")
    print("-------------")
    print("|", a21, "|", a22, "|", a23, "|")
    print("-------------")
    print("|", a31, "|", a32, "|", a33, "|")
    print("-------------")

    board = [[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]]
    check_win(board)

    return 0

def check_win(board):
    return 0

print("TIC-TAC-TOE")
print("\nInstructions:")
print("Two players, X and O, will take turns marking spaces in a 3x3 grid.")
print("The player who succeeds in placing three of their marks in a horizontal,")
print("vertical, or diagonal row wins the game.")

if (check_players() == True):
    play()
else:
    print("Thanks for playing. Restart to play again.")