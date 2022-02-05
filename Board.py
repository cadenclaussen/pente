import random
import sys


class Board:
    East = { 'name': 'east', 'yOffset': 0, 'xOffset': 1 }
    Southeast = { 'name': 'southeast', 'yOffset': 1, 'xOffset': 1 }
    South = { 'name': 'south', 'yOffset': 1, 'xOffset': 0 }
    Southwest = { 'name': 'southwest', 'yOffset': 1, 'xOffset': -1 }
    West = { 'name': 'west', 'yOffset': 0, 'xOffset': -1 }
    Northwest = { 'name': 'northwest', 'yOffset': -1, 'xOffset': -1 }
    North = { 'name': 'north', 'yOffset': -1, 'xOffset': 0 }
    Northeast = { 'name': 'northeast', 'yOffset': -1, 'xOffset': 1 }

    highlights = []
    opponentJumps = []
    points = {}
    winner = {}
    hint = {}


    def __init__(self, colors):

        # Load the patterns in from patterns.txt
        self.patterns = self.loadPatternDefinitions()

        # Save the colors
        self.colors = colors

        # Initialize each of the 19x19 positions on the board
        self.board = []
        for y in range(19):
            self.board.append([])
            for x in range(19):
                self.board[y].append({
                    'bead': 'Open',
                    'highlight': False,
                    'moves': [],
                    'weight': 0
                })

        # Initialize all the board metadata
        self.analyze(colors[0], colors[1], { 'x': 9, 'y': 9 }, 0)


    #--------------------------------------------------------------------------
    # Beads
    #--------------------------------------------------------------------------
    def addBead(self, x, y, color):
        self.board[y][x]['bead'] = color


    def removeBead(self, x, y):
        self.board[y][x]['bead'] = 'Open'


    def getBead(self, x, y):
        return self.board[y][x]['bead']


    def isOpen(self, x, y):
        return (self.board[y][x]['bead'] == 'Open')


    #--------------------------------------------------------------------------
    # Highlights
    #--------------------------------------------------------------------------
    def addHighlight(self, position):
        self.highlights.append(position)
        self.board[position['y']][position['x']]['highlight'] = True


    def getHighlight(self, x, y):
        return self.board[y][x]['highlight']


    def getHighlights(self):
        return self.highlights


    def clearHighlights(self):
        self.highlights = []
        for y in range(19):
            for x in range(19):
                self.board[y][x]['highlight'] = False


    def printAllHighlights(self):
        self.printHighlights(None)


    def printHighlights(self, category):
        print()
        if category is not None:
            print(category + ' positions:')
        for position in self.getHighlights():
            if category == None or category == position['category']:
                print(position['id'] + ' ' + self.xy(position['x'], position['y']))


    #--------------------------------------------------------------------------
    # Jumps
    #--------------------------------------------------------------------------
    def clearOpponentJumps(self):
        self.opponentJumps = []


    def addOpponentJump(self, position):
        print('Adding jump: ' + str(position))
        self.opponentJumps.append(position)


    def getOpponentJumps(self):
        return self.opponentJumps


    def printOpponentJumps(self):
        print()
        print('Opponent Jumps:')
        for position in self.opponentJumps:
            print('  ' + str(position))



    #--------------------------------------------------------------------------
    # Points
    #--------------------------------------------------------------------------
    def clearPoints(self):
        for color in self.colors:
            self.points[color] = 0

    def addPoints(self, color, points):
        self.points[color] += points

    def getPoints(self, color):
        return self.points[color]


    #--------------------------------------------------------------------------
    # Winner
    #--------------------------------------------------------------------------
    def clearWinner(self):
        for color in self.colors:
            self.winner[color] = False

    def setWinner(self, color):
        self.winner[color] = True

    def getWinner(self, color):
        return self.winner[color]


    #--------------------------------------------------------------------------
    # Moves
    #--------------------------------------------------------------------------
    def addMove(self, position):
        y = position['y']
        x = position['x']
        self.board[y][x]['moves'].append(position)
        self.board[y][x]['weight'] += position['weight']
        if self.board[y][x]['weight'] > self.getHint()['weight']:
            self.setHint(position['x'], position['y'], self.board[y][x]['weight'])


    def clearMoves(self):
        for y in range(19):
            for x in range(19):
                self.board[y][x]['moves'] = []
                self.board[y][x]['weight'] = 0


    def getMoves(self, x, y):
        return self.board[y][x]['moves']


    def getWeight(self, x, y):
        return self.board[y][x]['weight']


    def printMoves(self):
        for x in range(19):
            for y in range(19):
                if len(self.board[y][x]['moves']) > 0:
                    print(self.xy(x, y) + ': weight is ' + str(self.board[y][x]['weight']))
                    for position in self.board[y][x]['moves']:
                        print('  ' + str(position))


    #--------------------------------------------------------------------------
    # Hint
    #--------------------------------------------------------------------------
    def setHint(self, x, y, weight):
        self.hint = { 'x': x, 'y': y, 'weight': weight }


    def getHint(self):
        return self.hint


    def clearHint(self):
        self.setHint(9, 9, 0)


    def analyze(self, color, opponentColor, opponentLastMove, beadsPlayed):
        self.clearOpponentJumps()
        self.clearHighlights()
        self.clearMoves()
        self.clearWinner()
        self.clearPoints()
        self.clearHint()

        firstOpponentFiveOrMore = True
        firstFiveOrMore = True
        opponentPointPositions = {}
        pointPositions = {}
        for pattern in self.patterns:
            category = pattern['category']
            name = pattern['name']
            tokens = pattern['tokens']
            symmetric = pattern['symmetric']
            weight = pattern['weight']

            positions = self.findOnePatternAllPositionsAllDirections(pattern, color, opponentColor, opponentLastMove)

            if len(positions) == 0:
                continue

            if category == 'OpponentWin':
                self.setWinner(opponentColor)

            for position in positions:

                if category == 'OpponentJump':
                    self.addOpponentJump(position)
                    self.removeBead(position['x'], position['y'])

                elif category in [ 'OpponentWin', 'OpponentPoint', 'OpponentAnnounce', 'Point', 'Announce' ]:
                    self.addHighlight(position)
                    if category == 'OpponentPoint':
                        if position['id'] not in opponentPointPositions.keys():
                            opponentPointPositions[position['id']] = position['name']
                    if category == 'Point':
                        if position['id'] not in pointPositions.keys():
                            pointPositions[position['id']] = position['name']

                elif category in [ 'Defense', 'Offense' ]:
                    self.addMove(position)

        for color in [ { 'color': color, 'positions': pointPositions }, { 'color': opponentColor, 'positions': opponentPointPositions } ]:
            firstFiveOrMore = True
            for name in color['positions'].values():
                if name != '4' and firstFiveOrMore:
                    firstFiveOrMore = False
                else:
                    self.addPoints(color['color'], 1)

        if beadsPlayed == 0:
            position = { 'category': 'Openings', 'name': 'Opening', 'x': 9, 'y': 9, 'weight': 1 }
            self.addMove(position)

        elif beadsPlayed == 1:
            hintOptions = []
            for x in range(8, 11):
                for y in range(8, 11):
                    if x == 9 and y == 9:
                        continue
                    position = { 'category': 'Openings', 'name': 'Second', 'x': x, 'y': y, 'weight': 1 }
                    self.addMove(position)
                    hintOptions.append(position)
            hintChoice = random.choice(hintOptions)
            self.setHint(hintChoice['x'], hintChoice['y'], hintChoice['weight'])

        elif beadsPlayed == 2:
            hintOptions = []
            for x in range(6, 13):
                for y in range(6, 13):
                    self.board[y][x]['moves'] = []
                    self.board[y][x]['weight'] = 0
                    if x == 6 or x == 12 or y == 6 or y == 12:
                        position = { 'category': 'Openings', 'name': 'Third', 'x': x, 'y': y, 'weight': 1 }
                        self.addMove(position)
                        hintOptions.append(position)
            hintChoice = random.choice(hintOptions)
            self.setHint(hintChoice['x'], hintChoice['y'], hintChoice['weight'])


    def findOnePatternAllPositionsAllDirections(self, pattern, color, opponentColor, opponentLastMove):
        positions = []
        for x in range(-1, 20):
            for y in range(-1, 20):

                if pattern['category'] == 'OpponentJump' and (x != opponentLastMove['x'] or y != opponentLastMove['y']):
                    continue

                for direction in [ Board.East, Board.Southeast, Board.South, Board.Southwest ] if pattern['symmetric'] else [ Board.East, Board.Southeast, Board.South, Board.Southwest, Board.West, Board.Northwest, Board.North, Board.Northeast ]:

                    id = self.xyraw(x, y) + '-' + direction['name'] + '-' + pattern['category'] + '-' + pattern['name'] + '-' + str(pattern['weight'])

                    tmpX = x
                    tmpY = y
                    potentialPositions = []
                    for token in pattern['tokens']:

                        if not self.isTokenAtPosition(tmpX, tmpY, color, opponentColor, token):
                            potentialPositions = []
                            break

                        if token == 'P' or token == 'O' or token == 'C' or token == ',':
                            potentialPositions.append({ 'id': id, 'x': tmpX, 'y': tmpY, 'category': pattern['category'], 'name': pattern['name'], 'weight': pattern['weight'] })

                        tmpX += direction['xOffset']
                        tmpY += direction['yOffset']

                    if len(potentialPositions) > 0:
                        positions += potentialPositions

        return positions


    def isTokenAtPosition(self, x, y, color, opponentColor, token):

        # player
        #
        # matches a bead played at the position by the current player
        if token == 'p' or token == 'P':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if self.getBead(x, y) == color:
                return True
            return False

        # opponent
        #
        # matches a bead played at the position by an opposing player
        if token == 'o' or token == 'O':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if self.getBead(x, y) == opponentColor:
                return True
            return False

        # open
        #
        # matches a position with no bead
        if token == '.' or token == ',':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if self.isOpen(x, y):
                return True
            return False

        # not-player
        #
        # not-player means will match anything in the position other
        # than the current player's bead color including:
        # 1. a position that is off the board
        # 2. another player's bead
        # 3. an open position
        if token == '!':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return True
            if (self.getBead(x, y) != color):
                return True
            return False

        # not-opponent
        #
        # not-player means will match anything in the position other
        # than the current player's bead color including:
        # 1. a position that is off the board
        # 2. another player's bead
        # 3. an open position
        if token == '0':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return True
            if (self.getBead(x, y) != opponentColor):
                return True
            return False

        # closed
        #
        # Matches two scenarios:
        # 1. a position that is off the board
        # 2. a position occupied by an opposing player's bead
        if token == 'c' or token == 'C':
            if (x > 18 or x < 0 or y > 18 or y < 0):
                return True
            if not self.isOpen(x, y) and self.getBead(x, y) != color:
                return True
            return False

        print('board: we should never get here: token=' + token)
        sys.exit(1)


    def loadPatternDefinitions(self):
        with open('patterns.txt') as f:
            lines = f.readlines()

        patterns = []
        categoryLimit = 24
        nameLimit = 44
        tokensLimit = 71
        symmetricLimit = 72
        weightLimit = 75
        for line in lines:
            if line == '\n':
                continue
            category = ''
            name = ''
            tokens = ''
            symmetric = ''
            weight = ''
            n = -1
            for ch in line:
                n += 1
                if n < categoryLimit:
                    category += ch
                    continue
                if n < nameLimit:
                    name += ch
                    continue
                if n < tokensLimit:
                    tokens += ch
                    continue
                if n < symmetricLimit:
                    symmetric += ch
                    continue
                if n < weightLimit:
                    weight += ch
                    continue
                patterns.append({
                    'category': category.strip(),
                    'name': name.strip(),
                    'tokens': tokens.strip().split(),
                    'symmetric': True if symmetric.strip() == 'T' else False,
                    'weight': int(weight.strip())
                })
        return patterns


    def __str__(self):
        s = '\n   '
        for x in range(19):
            s += str(x  % 10) + '  '
        s += '\n'
        for y in range(19):
            s += str(y % 10)  + '  '
            for x in range(19):
                if self.isOpen(x, y):
                    if x == self.hint['x'] and y == self.hint['y']:
                        s += 'O  '
                    else:
                        s += '.  '
                    # weight = self.board[y][x]['weight']
                    # if x == self.hint['x'] and y == self.hint['y']:
                    #     s += 'O  '
                    # elif weight == 0:
                    #     s += '.  '
                    # elif weight > 0 and weight < 10:
                    #     s += str(self.board[y][x]['weight']) + '  '
                    # elif weight < -9:
                    #     s += '<  '
                    # else:
                    #     s += '>  '
                else:
                    if self.getHighlight(x, y):
                        s += self.getBead(x, y)[0] + '  '
                    else:
                        s += self.getBead(x, y)[0].lower() + '  '
            s += '\n'
        return s

    def xy(self, x, y):
        return '({0:>2}, {1:>2})'.format(x, y)

    def xyraw(self, x, y):
        return '{0},{1}'.format(x, y)
