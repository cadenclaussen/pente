import random
from Board import Board
from Match import Match


def testAll():
    tc('testAll')
    match = Match()
    match.newGame()
    generateRandomBoard(board, 150)
    print(board)
    board.analyze('Blue', 'Red', { 'x': 8, 'y': 8 })
    printMetadata(match)
    print(board)


def testBoard():
    tc('testBoard')
    match = Match()
    match.newGame()
    print(board)
    board.analyze('Blue', 'Red', { 'x': 8, 'y': 8 })
    print(board)
    printMetadata(match)
    board.printMoves()


def testWinningPatterns():
    tc('testWinningPatterns')
    match = Match()
    match.newGame()
    generateBeadSequence(match, 0, 0, Board.South, 9)
    generateBeadSequence(match, 16, 0, Board.South, 9)
    generateBeadSequence(match, 18, 0, Board.South, 9)
    generateBeadSequence(match, 0, 18, Board.East, 6)
    generateBeadSequence(match, 2, 2, Board.Southeast, 8)
    generateBeadSequence(match, 9, 9, Board.East, 7)
    generateBeadSequence(match, 9, 9, Board.South, 5)
    generateBeadSequence(match, 4, 4, Board.East, 3)
    generateBeadSequence(match, 6, 6, Board.East, 4)
    match.game.nextColor()
    match.game.board.analyze(match.game.currentColor, match.game.opponentColor, { 'x': 8, 'y': 8 }, 10)
    print(match)


def testPointPatterns():
    tc('testPointPatterns')
    match = Match()
    match.newGame()
    generateRandomBoard(match.game.board, 150)
    match.game.board.analyze('Red', 'Blue', { 'x': 8, 'y': 8 }, 150)
    print(match)


def testAnnouncePatterns():
    tc('testAnnouncePatterns')
    match = Match()
    match.newGame()
    generateRandomBoard(board, 150)
    board.analyze(match.game.currentColor, match.game.opponentColor, { 'x': 8, 'y': 8 }, 150)
    print(match)


def testJumpPatterns():
    tc('testJumpPatterns')
    match = Match()
    generateJumpPattern(board, 9, 9, Board.North)
    generateJumpPattern(board, 9, 9, Board.Northeast)
    generateJumpPattern(board, 9, 9, Board.East)
    generateJumpPattern(board, 9, 9, Board.Southeast)
    generateJumpPattern(board, 9, 9, Board.South)
    generateJumpPattern(board, 9, 9, Board.Southwest)
    generateJumpPattern(board, 9, 9, Board.West)
    generateJumpPattern(board, 9, 9, Board.Northwest)
    board.analyze('Red', 'Blue', { 'x': 9, 'y': 9 }, 100)
    print(match)


def testMovePatterns():
    tc('testMovePatterns')
    match = Match()
    generateRandomBoard(board, 150)
    board.analyze('Red', 'Blue', { 'x': 9, 'y': 9 }, 100)
    print(board)
    printMetadata([], board)
    board.printMoves()


def printMetadata(match):
    board = match.game.board
    board.printAnnounces()
    print()
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


def tc(name):
    print()
    print(name)
    print()


def generateBeadSequence(match, x, y, direction, count):
    for i in range(count):
        match.game.board.addBead(x + direction['xOffset'] * i, y + direction['yOffset'] * i, match.game.currentColor)
        match.game.nextColor()
        match.game.nextColor()


def generateJumpPattern(board, x, y, direction):
    board.addBead(x, y, 'Blue')
    board.addBead(x + direction['xOffset'], y + direction['yOffset'], 'Red')
    board.addBead(x + (2 * direction['xOffset']), y + (2 * direction['yOffset']), 'Red')
    board.addBead(x + (3 * direction['xOffset']), y + (3 * direction['yOffset']), 'Blue')


def generateRandomBoard(board, numberOfTurns):
    color = 'Blue'
    for _ in range(numberOfTurns):
        while True:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            if board.isOpen(x, y):
                break
        board.addBead(x, y, color)
        if color == 'Red':
            color = 'Blue'
        else:
            color = 'Red'


def xy(x, y):
    return '{0:>2} {1:>2}'.format(x, y) + ': '


# testAll()
testWinningPatterns()
# testPointPatterns()
# testAnnouncePatterns()
# testJumpPatterns()
# testMovePatterns()
