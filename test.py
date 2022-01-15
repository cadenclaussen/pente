import random
from Board import Board
from Player import Player
from Game import Game


def testWinningPatterns():
    print()
    print("testWinningPatterns")
    game, board, players, currentPlayer = __init()
    __generateBeadsInARow(board, { "row": 0, "column": 0 }, Board.South, 9)
    __generateBeadsInARow(board, { "row": 0, "column": 18 }, Board.South, 9)
    __generateBeadsInARow(board, { "row": 2, "column": 2 }, Board.Southeast, 8)
    __generateBeadsInARow(board, { "row": 9, "column": 9 }, Board.East, 7)
    __generateBeadsInARow(board, { "row": 9, "column": 9 }, Board.South, 5)
    __generateBeadsInARow(board, { "row": 4, "column": 4 }, Board.East, 3)
    __generateBeadsInARow(board, { "row": 6, "column": 6 }, Board.East, 4)
    __printWinningPatterns(board, players, currentPlayer)


def testJumpPatterns():
    print()
    print("testJumpPatterns")
    game, board, players, currentPlayer = __init()
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.North)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.Northeast)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.East)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.Southeast)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.South)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.Southwest)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.West)
    __generateJumpPattern(board, { "row": 9, "column": 9 }, Board.Northwest)
    __printJumpPatterns(board, players, currentPlayer)


def testAnnouncePatterns():
    print()
    print("testAnnouncePatterns")
    game, board, players, currentPlayer = __init()
    __generateRandomBoard(board, players, 150)
    __printWinningPatterns(board, players, currentPlayer)
    __printAnnouncePatterns(board, players, currentPlayer)


def testPointPatterns():
    print()
    print("testPointPatterns")
    game, board, players, currentPlayer = __init()
    __generateRandomBoard(board, players, 150)
    __printPointPatterns(board, players, currentPlayer)


def __printWinningPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print("Winning Patterns")
    board.findWinningPatterns(currentPlayer)
    for winningPattern in board.winningPatterns:
        print(winningPattern["name"] + __positions(winningPattern["positions"]))


def __printJumpPatterns(board, players, currentPlayer):
    print()
    board.findJumpPatterns(currentPlayer, { "row": 9, "column": 9 })
    print(board)
    print()
    print("Jump Patterns")
    for jumpPattern in board.jumpPatterns:
        print(__positions(jumpPattern["positions"]))


def __printAnnouncePatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print("Announce Patterns")
    board.findAnnouncePatterns(players[0])
    for announcePattern in board.announcePatterns[players[0].name]:
        print(players[0].name + ": " + announcePattern["name"] + __positions(announcePattern["positions"]))
    board.findAnnouncePatterns(players[1])
    for announcePattern in board.announcePatterns[players[1].name]:
        print(players[1].name + ": " + announcePattern["name"] + __positions(announcePattern["positions"]))


def __printPointPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print("Point Patterns")
    board.findPointPatterns(players[0])
    for pointPattern in board.pointPatterns[players[0].name]:
        print(players[0].name + ": " + pointPattern["name"] + __positions(pointPattern["positions"]))
    board.findPointPatterns(players[1])
    for pointPattern in board.pointPatterns[players[1].name]:
        print(players[1].name + ": " + pointPattern["name"] + __positions(pointPattern["positions"]))


def __positions(positions):
    s = ""
    for position in positions:
        s += " (" + str(position["column"]) + "," + str(position["row"]) + ")"
    return s


def __init():
    player1 = Player("Shane", "Blue", 0)
    player2 = Player("Caden", "Red", 1)
    return Game(), Board(), [ player1, player2], player1


def __generateBeadsInARow(board, position, direction, count):
    for i in range(count):
        board.board[position["column"] + (direction["columnOffset"] * i)][position["row"] + (direction["rowOffset"] * i)] = "B"


def __generateJumpPattern(board, position, direction):
    board.board[position["column"]][position["row"]] = 'B'
    board.board[position["column"] + direction["columnOffset"]][position["row"] + direction["rowOffset"]] = 'R'
    board.board[position["column"] + (2 * direction["columnOffset"])][position["row"] + (2 * direction["rowOffset"])] = 'R'
    board.board[position["column"] + (3 * direction["columnOffset"])][position["row"] + (3 * direction["rowOffset"])] = 'B'


def __generateRandomBoard(board, players, numberOfTurns):
    currentPlayer = players[0]
    for _ in range(numberOfTurns):
        while True:
            row = random.randint(0, 18)
            column = random.randint(0, 18)
            if board.board[column][row] == '.':
                break
        board.board[column][row] = currentPlayer.color[0]
        if currentPlayer.key == 0:
            currentPlayer = players[1]
        else:
            currentPlayer = players[0]


testWinningPatterns()
testJumpPatterns()
testAnnouncePatterns()
testPointPatterns()
