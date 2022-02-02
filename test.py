import random
from Board import Board
from Player import Player
from Match import Match


def testAll():
    tc('testAll')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    print(board)
    board.analyze('Blue', 'Red', { 'x': 8, 'y': 8 })
    printMetadata( [ 'OpponentWin', 'OpponentPoint', 'OpponentAnnounce', 'Point', 'Announce' ], board)
    print(board)

def testBoard():
    tc('testBoard')
    match, board, players, currentPlayer = init()
    print(board)
    board.analyze('Blue', 'Red', { 'x': 8, 'y': 8 })
    print(board)
    printMetadata([], board)
    board.printMoves()


def testWinningPatterns():
    tc('testWinningPatterns')
    match, board, players, currentPlayer = init()
    generateBeadSequence(board, 0, 0, Board.South, 9, 'Blue')
    generateBeadSequence(board, 16, 0, Board.South, 9, 'Blue')
    generateBeadSequence(board, 18, 0, Board.South, 9, 'Blue')
    generateBeadSequence(board, 0, 18, Board.East, 6, 'Blue')
    generateBeadSequence(board, 2, 2, Board.Southeast, 8, 'Blue')
    generateBeadSequence(board, 9, 9, Board.East, 7, 'Blue')
    generateBeadSequence(board, 9, 9, Board.South, 5, 'Blue')
    generateBeadSequence(board, 4, 4, Board.East, 3, 'Blue')
    generateBeadSequence(board, 6, 6, Board.East, 4, 'Blue')
    board.analyze('Red', 'Blue', { 'x': 8, 'y': 8 })
    print(board)
    printMetadata([ 'OpponentWin' ], board)


def testPointPatterns():
    tc('testPointPatterns')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    board.analyze('Red', 'Blue', { 'x': 8, 'y': 8 })
    print(board)
    printMetadata([ 'Point', 'OpponentPoint' ], board)


def testAnnouncePatterns():
    tc('testAnnouncePatterns')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    board.analyze('Red', 'Blue', { 'x': 8, 'y': 8 })
    print(board)
    board.printHighlights
    printMetadata([ 'Announce', 'OpponentAnnounce' ], board)


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
    board.analyze('Red', 'Blue', { 'x': 9, 'y': 9 })
    print(board)
    printMetadata([], board)


def testMovePatterns():
    tc('testMovePatterns')
    match, board, players, currentPlayer = init()
    generateRandomBoard(board, players, 150)
    board.analyze('Red', 'Blue', { 'x': 9, 'y': 9 })
    print(board)
    printMetadata([], board)
    board.printMoves()


def printMetadata(highlights, board):
    for highlight in highlights:
        board.printHighlights(highlight)
    print()
    # print('highlights: ' + str(board.getHighlights()))
    print('jumps: ' + str(board.getOpponentJumps()))
    print('points[Blue]: ' + str(board.getPoints('Blue')))
    print('points[Red]: ' + str(board.getPoints('Red')))
    print('winner[Blue]: ' + str(board.getWinner('Blue')))
    print('winner[Red]: ' + str(board.getWinner('Red')))
    print('hint: ' + str(board.getHint()))


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


def generateBeadSequence(board, x, y, direction, count, color):
    for i in range(count):
        board.addBead(x + direction['xOffset'] * i, y + direction['yOffset'] * i, color)


def generateJumpPattern(board, x, y, direction):
    board.addBead(x, y, 'Blue')
    board.addBead(x + direction['xOffset'], y + direction['yOffset'], 'Red')
    board.addBead(x + (2 * direction['xOffset']), y + (2 * direction['yOffset']), 'Red')
    board.addBead(x + (3 * direction['xOffset']), y + (3 * direction['yOffset']), 'Blue')


def generateRandomBoard(board, players, numberOfTurns):
    currentPlayer = players[0]
    for _ in range(numberOfTurns):
        while True:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            if board.isOpen(x, y):
                break
        board.addBead(x, y, currentPlayer.color)
        if currentPlayer.key == 0:
            currentPlayer = players[1]
        else:
            currentPlayer = players[0]


def xy(x, y):
    return '{0:>2} {1:>2}'.format(x, y) + ': '


# testAll()
# testWinningPatterns()
# testPointPatterns()
# testAnnouncePatterns()
testJumpPatterns()
# testMovePatterns()
