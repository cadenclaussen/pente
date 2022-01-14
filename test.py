import random
from Board import Board
from Player import Player
from Game import Game


def main():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    player2 = Player("Caden", "Red", 1)
    players = [ player1, player2 ]
    game = Game()
    positionsFound = []
    generateRandomBoard(board, players, 150)
    for row in range(19):
        for col in range(19):
            positionsFound.append(board.findJumpPatterns(player1, { "row": row, "column": col }))
            positionsFound.append(board.findJumpPatterns(player2, { "row": row, "column": col }))
    print(positionsFound)
    print()
    print(board)


def testWinning():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    currentPlayer = player1
    game = Game()
    generateFive(board, 9, 9, 0, 1)
    generateFive(board, 9, 9, 1, 0)
    winningPatterns = board.findWinningPatterns(currentPlayer)
    print(winningPatterns)
    if winningPatterns != []:
        game.winner = True
    print(board)


def generateFive(board, row, col, rowOffset, columnOffset):
    board.board[row][col] = "B"
    board.board[row + rowOffset][col + columnOffset] = "B"
    board.board[row + 2 * rowOffset][col + 2 * columnOffset] = "B"
    board.board[row + 3 * rowOffset][col + 3 * columnOffset] = "B"
    board.board[row + 4 * rowOffset][col + 4 * columnOffset] = "B"


def testJumps():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    currentPlayer = player1
    generateJumps(board)
    jumps = board.findJumpPatterns(currentPlayer, { "row": 9, "column": 9 })
    print(jumps)
    print("")
    for i in range(8):
        print(str(jumps[0][i]["pattern"]["direction"]), str(jumps[0][i]["positions"][0]), str(jumps[0][i]["positions"][1]))
    print('Removing jumps')
    for i in range(2):
        print(str(jumps[0][0]["positions"][i - 1]))

    for i in range(2):
        for j in range(8):
            print(str(jumps[0][j]["positions"][i]))
            board.removeFromBoard(str(jumps[0][j]["positions"][i]))

    if jumps != []:
        currentPlayer.jumps += len(jumps)
    if currentPlayer.jumps >= 5:
        game.winner = True
    print(board)



def generateJumps(board):
    __createJump(board, 9, 9, 0, 1)
    __createJump(board, 9, 9, 1, 0)
    __createJump(board, 9, 9, 1, 1)
    __createJump(board, 9, 9, -1, 0)
    __createJump(board, 9, 9, -1, 1)
    __createJump(board, 9, 9, 1, -1)
    __createJump(board, 9, 9, 0, -1)
    __createJump(board, 9, 9, -1, -1)
    return board


def __createJump(board, row, column, rowOffset, columnOffset):
    board.board[row][column] = 'B'
    board.board[row + rowOffset][column + columnOffset] = 'R'
    board.board[row + (2 * rowOffset)][column + (2 * columnOffset)] = 'R'
    board.board[row + (3 * rowOffset)][column + (3 * columnOffset)] = 'B'


def generateRandomBoard(board, players, numberOfTurns):
    currentPlayer = players[0]
    for _ in range(numberOfTurns):
        while True:
            row = random.randint(0, 18)
            col = random.randint(0, 18)
            if board.board[row][col] == '.':
                break
        board.board[col][row] = currentPlayer.color[0]
        if currentPlayer.key == 0:
            currentPlayer = players[1]
        else:
            currentPlayer = players[0]


def generateCreatedBoard(board):
    board.board[1][1] = "B"
    board.board[1][2] = "R"
    board.board[1][3] = "R"
    board.board[1][4] = "R"
    board.board[1][5] = "R"


testJumps()
