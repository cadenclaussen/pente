import random
from Board import Board
from Player import Player
from Game import Game


def testBoard():
    print()
    print('testBoard')
    print()
    game, board, players, currentPlayer = __init()
    print(board)


def testWinningPatterns():
    print()
    print('testWinningPatterns')
    print()
    game, board, players, currentPlayer = __init()
    __generateBeadSequence(board, 0, 0, Board.South, 9)
    __generateBeadSequence(board, 18, 0, Board.South, 9)
    __generateBeadSequence(board, 0, 18, Board.East, 6)
    __generateBeadSequence(board, 2, 2, Board.Southeast, 8)
    __generateBeadSequence(board, 9, 9, Board.East, 7)
    __generateBeadSequence(board, 9, 9, Board.South, 5)
    __generateBeadSequence(board, 4, 4, Board.East, 3)
    __generateBeadSequence(board, 6, 6, Board.East, 4)
    __printWinningPatterns(board, players, currentPlayer)


def testJumpPatterns():
    print()
    print('testJumpPatterns')
    print()
    game, board, players, currentPlayer = __init()
    __generateJumpPattern(board, 9, 9, Board.North)
    __generateJumpPattern(board, 9, 9, Board.Northeast)
    __generateJumpPattern(board, 9, 9, Board.East)
    __generateJumpPattern(board, 9, 9, Board.Southeast)
    __generateJumpPattern(board, 9, 9, Board.South)
    __generateJumpPattern(board, 9, 9, Board.Southwest)
    __generateJumpPattern(board, 9, 9, Board.West)
    __generateJumpPattern(board, 9, 9, Board.Northwest)
    __printJumpPatterns(board, players, currentPlayer)


def testAnnouncePatterns():
    print()
    print('testAnnouncePatterns')
    print()
    game, board, players, currentPlayer = __init()
    __printWinningPatterns(board, players, currentPlayer)
    __printAnnouncePatterns(board, players, currentPlayer)


def testPointPatterns():
    print()
    print('testPointPatterns')
    print()
    game, board, players, currentPlayer = __init()
    __generateRandomBoard(board, players, 150)
    __printPointPatterns(board, players, currentPlayer)


def __printWinningPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Winning Patterns')
    board.findWinningPatterns(currentPlayer)
    for winningPattern in board.winningPatterns:
        print(winningPattern['name'] + __positions(winningPattern['positions']))


def __printJumpPatterns(board, players, currentPlayer):
    print()
    board.findJumpPatterns(currentPlayer, x, y)
    print()
    print(board)
    print()
    print('Jump Patterns')
    for jumpPattern in board.jumpPatterns:
        print(__positions(jumpPattern['positions']))


def __printAnnouncePatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Announce Patterns')
    board.findAnnouncePatterns(players[0])
    for announcePattern in board.announcePatterns[players[0].name]:
        print(players[0].name + ': ' + announcePattern['name'] + __positions(announcePattern['positions']))
    board.findAnnouncePatterns(players[1])
    for announcePattern in board.announcePatterns[players[1].name]:
        print(players[1].name + ': ' + announcePattern['name'] + __positions(announcePattern['positions']))


def __printPointPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Point Patterns')
    board.findPointPatterns(players[0])
    for pointPattern in board.pointPatterns[players[0].name]:
        print(players[0].name + ': ' + pointPattern['name'] + __positions(pointPattern['positions']))
    board.findPointPatterns(players[1])
    for pointPattern in board.pointPatterns[players[1].name]:
        print(players[1].name + ': ' + pointPattern['name'] + __positions(pointPattern['positions']))


def __positions(positions):
    s = ''
    for position in positions:
        s += ' (' + str(position['x']) + ',' + str(position['y']) + ')'
    return s


def __init():
    player1 = Player('Shane', 'Blue', 0)
    player2 = Player('Caden', 'Red', 1)
    return Game(), Board(), [ player1, player2], player1


def __generateBeadSequence(board, x, y, direction, count):
    for i in range(count):
        board.playBead(x + direction['xOffset'] * i, y + direction['yOffset'] * i, 'Blue')


def __generateJumpPattern(board, x, y, direction):
    board.playBead(x, y, 'Blue')
    board.playBead(x + direction['xOffset'], y + direction['yOffset'], 'Red')
    board.playBead(x + (2 * direction['xOffset']), y + (2 * direction['yOffset']), 'Red')
    board.playBead(x + (3 * direction['xOffset']), y + (3 * direction['yOffset']), 'Blue')


def __generateRandomBoard(board, players, numberOfTurns):
    currentPlayer = players[0]
    for _ in range(numberOfTurns):
        while True:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            if board.getBead(x, y) == 'Open':
                break
        board.playBead(x, y, currentPlayer.color)
        if currentPlayer.key == 0:
            currentPlayer = players[1]
        else:
            currentPlayer = players[0]


# testBoard()
testWinningPatterns()
# testJumpPatterns()
# testAnnouncePatterns()
# testPointPatterns()
