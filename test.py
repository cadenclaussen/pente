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
            board.findJumpPatterns(player1, { "row": row, "col": col })
            board.findJumpPatterns(player2, { "row": row, "col": col })
    # board.findPatternsToAnnounce(player1)
    # board.findPatternsToAnnounce(player2)
    print()
    print(board)


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


main()
