import random
import sys

board = None

def main():
    board = initializeBoard()
    token = random.choice(["R", "B"])
    printBoard(board)
    board = generateRandomBoard(board, token, 200)
    for i in range(5):
        print(" ")
    printBoard(board)
    isPatterns(board, "R")
    isPatterns(board, "B")


def newGame():
    global board
    board = None
    board = initializeBoard()
    printBoard(board)

def getColorFirst():
    return random.randint(0, 1)

def beadPlayed(color, position):
    global board
    isWinningPatterns(board, color)
    color = switchTurns(color)
    patternsFound = isCommonPatterns(board, color)
    #suggestions = suggestOptions(board)
    printOntoBoard(board, position, color)
    return patternsFound

def printOntoBoard(board, position, color):
    if color == 1:
        color = "B"
    if color == 0:
        color = "R"
    board[position["row"]][position["col"]] = color
    printBoard(board)

def suggestOptions(board):
    pass

def initializeBoard():
    blueJumps = 0
    redJumps = 0
    print("Initializing board")
    board = []
    for row in range(19):
        board.append([])
        for col in range(19):
            board[row].append(".")
    return board

def printBoard(board):
    print("   ", end="")
    for col in range(19):
        print(str(col  % 10) + "   ", end="")
    print()
    for row in range(19):
        print(str(row % 10)  + "  ", end="")
        for col in range(19):
            print(str(board[row][col]) + "   ", end="")
        print(" ")

def switchTurns(token):
    if token == 1:
        return 0
    else:
        return 1
