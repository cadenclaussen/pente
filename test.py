import random
from Board import Board
from Player import Player
from Match import Match


def testBoard():
    tc('testBoard')
    match, board, players, currentPlayer = init()
    print(board)


def testWinningPatterns():
    tc('testWinningPatterns')
    match, board, players, currentPlayer = init()
    generateBeadSequence(board, 0, 0, Board.South, 9)
    generateBeadSequence(board, 18, 0, Board.South, 9)
    generateBeadSequence(board, 0, 18, Board.East, 6)
    generateBeadSequence(board, 2, 2, Board.Southeast, 8)
    generateBeadSequence(board, 9, 9, Board.East, 7)
    generateBeadSequence(board, 9, 9, Board.South, 5)
    generateBeadSequence(board, 4, 4, Board.East, 3)
    generateBeadSequence(board, 6, 6, Board.East, 4)
    printWinningPatterns(board, players, currentPlayer)


def testJumpPatterns():
    tc('testJumpPatterns')
    match, board, players, currentPlayer = init()
    generateJumpPattern(board, 9, 9, Board.North)
    generateJumpPattern(board, 9, 9, Board.Northeast)
    generateJumpPattern(board, 9, 9, Board.East)
    generateJumpPattern(board, 9, 9, Board.Southeast)
    generateJumpPattern(board, 9, 9, Board.South)
    generateJumpPattern(board, 9, 9, Board.Southwest)
    generateJumpPattern(board, 9, 9, Board.West)
    generateJumpPattern(board, 9, 9, Board.Northwest)
    printJumpPatterns(board, 9, 9, players, currentPlayer)


def testAnnouncePatterns():
    tc('testAnnouncePatterns')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    printAnnouncePatterns(board, players, currentPlayer.color)


def testMovePatterns():
    tc('testMovePatterns')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    printMovePatterns(board, players, currentPlayer.color)


def testPointPatterns():
    print()
    print('testPointPatterns')
    print()
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    printPointPatterns(board, players, currentPlayer.color)


def printWinningPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Winning Patterns')
    # board.findPattern('Blue', { 'name': 'Nine', 'tokens': [ 'not-bead', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'bead:save', 'not-bead' ] }, None)
    board.findWinningPatterns(currentPlayer.color)
    for winningPattern in board.winningPatterns:
        print(winningPattern['name'] + positions(winningPattern['positions']))


def printJumpPatterns(board, x, y, players, currentPlayer):
    print()
    board.findJumpPatterns(x, y, currentPlayer.color)
    print()
    print(board)
    print()
    print('Jump Patterns')
    for jumpPattern in board.jumpPatterns:
        print(positions(jumpPattern['positions']))


def printAnnouncePatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Announce Patterns')
    board.findAnnouncePatterns(players[0].color)
    for announcePattern in board.announcePatterns[players[0].color]:
        print(players[0].color + ': ' + announcePattern['name'] + positions(announcePattern['positions']))
    board.findAnnouncePatterns(players[1].color)
    for announcePattern in board.announcePatterns[players[1].color]:
        print(players[1].color + ': ' + announcePattern['name'] + positions(announcePattern['positions']))


def printMovePatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Move Patterns')
    board.findMovePatterns(players[0].color)
    for movePattern in board.movePatterns[players[0].color]:
        print(players[0].color + ': ' + movePattern['name'] + positions(movePattern['positions']))
    board.findMovePatterns(players[1].color)
    for movePattern in board.movePatterns[players[1].color]:
        print(players[1].color + ': ' + movePattern['name'] + positions(movePattern['positions']))


def printPointPatterns(board, players, currentPlayer):
    print()
    print(board)
    print()
    print('Point Patterns')
    board.findPointPatterns(players[0].color)
    for pointPattern in board.pointPatterns[players[0].color]:
        print(players[0].color + ': ' + pointPattern['name'] + positions(pointPattern['positions']))
    board.findPointPatterns(players[1].color)
    for pointPattern in board.pointPatterns[players[1].color]:
        print(players[1].color + ': ' + pointPattern['name'] + positions(pointPattern['positions']))


def positions(positions):
    s = ''
    for position in positions:
        s += ' (' + str(position['x']) + ',' + str(position['y']) + ')'
    return s


def init():
    player1 = Player('Shane', 'Blue', 0)
    player2 = Player('Caden', 'Red', 1)
    players = [ player1, player2 ]
    return Match(), Board(players), players, player1


def tc(name):
    print()
    print(name)
    print()


def generateBeadSequence(board, x, y, direction, count):
    for i in range(count):
        board.playBead(x + direction['xOffset'] * i, y + direction['yOffset'] * i, 'Blue')


def generateJumpPattern(board, x, y, direction):
    board.playBead(x, y, 'Blue')
    board.playBead(x + direction['xOffset'], y + direction['yOffset'], 'Red')
    board.playBead(x + (2 * direction['xOffset']), y + (2 * direction['yOffset']), 'Red')
    board.playBead(x + (3 * direction['xOffset']), y + (3 * direction['yOffset']), 'Blue')


def generateRandomBoard(board, players, numberOfTurns):
    currentPlayer = players[0]
    for _ in range(numberOfTurns):
        while True:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            if board.isOpen(x, y):
                break
        board.playBead(x, y, currentPlayer.color)
        if currentPlayer.key == 0:
            currentPlayer = players[1]
        else:
            currentPlayer = players[0]


# testBoard()
# testWinningPatterns()
# testJumpPatterns()
# testAnnouncePatterns()
testMovePatterns()
# testPointPatterns()
