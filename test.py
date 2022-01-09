import random
from Board import Board
from Player import Player


def main():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    player2 = Player("Caden", "Red", 1)
    players = [ player1, player2 ]
    generateRandomBoard(board, players, 150)
    # board.findWinningPatterns(player1)
    # board.findWinningPatterns(player2)
    for row in range(19):
        for col in range(19):
            board.findJumpPatterns(player1, { "row": row, "column": col })
            board.findJumpPatterns(player2, { "row": row, "column": col })
    # board.findPatternsToAnnounce(player1)
    # board.findPatternsToAnnounce(player2)
    print()
    print(board)


def testWinning():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    currentPlayer = player1
    generateFive(board)
    winningPatterns = board.findWinningPatterns(currentPlayer, { "row": 9, "column": 9 })
    print(winningPatterns)
    print(board)


def testJumps():
    board = Board()
    player1 = Player("Shane", "Blue", 0)
    currentPlayer = player1
    generateJumps(board)
    jumps =  board.findJumpPatterns(currentPlayer, { "row": 9, "column": 9 })
    print(jumps)
    print(board)


def generateJumps(board):
    __createJump(board, 9, 9, 0, 1)
    __createJump(board, 9, 9, 1, 0)
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
