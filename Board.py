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


    def __init__(self, players):
        self.jumpPatterns = []
        self.winningPatterns = []
        self.players = players

        self.announcePatterns = {}
        self.offensePatterns = {}
        self.pointPatterns = {}
        for player in players:
            self.announcePatterns[player.color] = []
            self.offensePatterns[player.color] = []
            self.pointPatterns[player.color] = []

        self.board = []
        for y in range(19):
            self.board.append([])
            for x in range(19):
                self.board[y].append({ 'bead': 'Open', 'beadHighlight': False, 'moveHighlight': False, 'weight': 0 })


    def playBead(self, x, y, color):
        self.board[y][x]['bead'] = color


    def removeBead(self, x, y):
        self.board[y][x]['bead'] = 'Open'


    def getBead(self, x, y):
        return self.board[y][x]['bead']


    def getBeadHighlight(self, x, y):
        return self.board[y][x]['beadHighlight']


    def setBeadHighlight(self, x, y):
        self.board[y][x]['beadHighlight'] = True


    def clearBeadHighlights(self, color):
        for y in range(19):
            for x in range(19):
                if self.getBead(x, y) == color:
                    self.board[y][x]['beadHighlight'] = False


    def getMoveHighlight(self, x, y):
        return self.board[y][x]['moveHighlight']


    def setMoveHighlight(self, x, y):
        self.board[y][x]['moveHighlight'] = True


    def clearMoveHighlights(self, color):
        for y in range(19):
            for x in range(19):
                if self.getBead(x, y) == color:
                    self.board[y][x]['moveHighlight'] = False


    def isOpen(self, x, y):
        return (self.board[y][x]['bead'] == 'Open')


    def findJumpPatterns(self, x, y, color):
        self.jumpPatterns = []

        patterns = []
        patterns.append({ 'name': 'Jump', 'tokens': [ 'bead', 'opponent:s', 'opponent:s', 'bead' ]})

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.findPatternAtPosition(x, y, color, patterns[0], [ Board.East, Board.Southeast, Board.South, Board.Southwest, Board.West, Board.Northwest, Board.North, Board.Northeast ])
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.jumpPatterns = cumulativePatternsFound
        for jumpPattern in self.jumpPatterns:
            for position in jumpPattern['positions']:
                self.removeBead(position['x'], position['y'])

        return self.jumpPatterns != []


    def findWinningPatterns(self, color):
        self.winningPatterns = []

        patterns = []
        patterns.append({ 'name': 'Five', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Six', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Seven', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Eight', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Nine', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.winningPatterns = cumulativePatternsFound
        return self.winningPatterns != []


    def findAnnouncePatterns(self, color):
        self.clearBeadHighlights(color)
        self.announcePatterns[color] = []

        patterns = []
        patterns.append({ 'name': 'Open Three', 'tokens': [ 'not-bead', 'open', 'bead:s', 'bead:s', 'bead:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'not-bead', 'open', 'bead:s', 'open', 'bead:s', 'bead:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'not-bead', 'open', 'bead:s', 'bead:s', 'open', 'bead:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Closed Four', 'tokens': [ 'not-bead', 'open', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'closed' ] })
        patterns.append({ 'name': 'Closed Four', 'tokens': [ 'closed', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Open Four', 'tokens': [ 'not-bead', 'open', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead:s', 'open', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'open', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'open', 'bead:s', 'not-bead' ] })
        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                cumulativePatternsFound += patternsFound

        patterns = []
        patterns.append({ 'name': 'Jump', 'tokens': [ 'bead', 'opponent:s', 'opponent:s', 'open' ]})
        patterns.append({ 'name': 'Jump', 'tokens': [ 'open', 'opponent:s', 'opponent:s', 'bead' ]})
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.announcePatterns[color] = cumulativePatternsFound

        for announcePattern in self.announcePatterns[color]:
            for position in announcePattern['positions']:
                self.setBeadHighlight(position['x'], position['y'])

        return self.announcePatterns[color] != []


    def findPointPatterns(self, color):
        self.pointPatterns[color] = []

        patterns = []
        patterns.append({ 'name': 'Four', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                cumulativePatternsFound += patternsFound

        # Having 5 or more beads in a row is a winning sequence and the
        # player gets 5 points (logic for that is not handled here).
        #
        # However, if the player adds a bead that results in more than
        # one 5+ sequence of beads, they get the win and 5 points for
        # the first, but for every subsequent bead they get a single
        # point.
        firstWinningPattern = True
        patterns = []
        patterns.append({ 'name': 'Five', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Six', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Seven', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Eight', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        patterns.append({ 'name': 'Nine', 'tokens': [ 'not-bead', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'bead:s', 'not-bead' ] })
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                if firstWinningPattern:
                    firstWinningPattern = False
                    continue
                cumulativePatternsFound += patternsFound

        self.pointPatterns[color] = cumulativePatternsFound
        return self.pointPatterns[color] != []


    def findOffensePatterns(self, color):
        for player in self.players:
            self.clearMoveHighlights(player.color)
            self.offensePatterns[player.color] = []

        patterns = []

        # Defensive
        # patterns.append({ 'name': 'Open Three', 'tokens': [ 'not-bead', 'open:s', 'bead', 'bead', 'bead', 'open:s', 'not-bead' ] })
        # patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'not-bead', 'open:s', 'bead', 'open', 'bead', 'bead', 'open:s', 'not-bead' ] })
        # patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'not-bead', 'open:s', 'bead', 'bead', 'open', 'bead', 'open:s', 'not-bead' ] })
        # patterns.append({ 'name': 'Closed Four', 'tokens': [ 'not-bead', 'open:s', 'bead', 'bead', 'bead', 'bead', 'closed' ] })
        # patterns.append({ 'name': 'Closed Four', 'tokens': [ 'closed', 'bead', 'bead', 'bead', 'bead', 'open:s', 'not-bead' ] })
        # patterns.append({ 'name': 'Open Four', 'tokens': [ 'not-bead', 'open:s', 'bead', 'bead', 'bead', 'bead', 'open:s', 'not-bead' ] })
        # patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'open:s', 'bead', 'bead', 'bead', 'not-bead' ] })
        # patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'open:s', 'bead', 'bead', 'not-bead' ] })
        # patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'open:s', 'bead', 'not-bead' ] })

        # Offense
        patterns.append({ 'name': 'Jump', 'tokens': [ 'bead', 'opponent', 'opponent', 'open:s' ]})
        patterns.append({ 'name': 'Jump', 'tokens': [ 'open:s', 'opponent', 'opponent', 'bead' ]})
        patterns.append({ 'name': 'Potential Holed Open Four', 'tokens': [ 'not-bead', 'open', 'bead', 'open:s', 'open:s', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'closed', 'open:s', 'bead', 'bead', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'closed', 'bead', 'open:s', 'bead', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'closed', 'bead', 'bead', 'open:s', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'closed', 'bead', 'bead', 'bead', 'open:s', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'not-bead', 'open', 'bead', 'bead', 'bead', 'open:s', 'closed' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'not-bead', 'open', 'bead', 'bead', 'open:s', 'bead', 'closed' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'not-bead', 'open', 'bead', 'open:s', 'bead', 'bead', 'closed' ] })
        patterns.append({ 'name': 'Potential Closed Four', 'tokens': [ 'not-bead', 'open', 'open:s', 'bead', 'bead', 'bead', 'closed' ] })
        patterns.append({ 'name': 'Potential Open Three', 'tokens': [ 'not-bead', 'open', 'bead', 'open:s', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Potential Open Three', 'tokens': [ 'open', 'open:s', 'bead', 'bead', 'open:s', 'open' ]})
        patterns.append({ 'name': 'Potential Jump', 'tokens': [ 'open:s', 'opponent', 'opponent', 'open' ]})
        patterns.append({ 'name': 'Potential Jump', 'tokens': [ 'open', 'opponent', 'opponent', 'open:s' ]})

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.findPattern(color, pattern)
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.offensePatterns[color] = cumulativePatternsFound

        for offensePattern in self.offensePatterns[color]:
            for position in offensePattern['positions']:
                self.setMoveHighlight(position['x'], position['y'])

        return self.offensePatterns[color] != []


    def findPattern(self, color, pattern):
        cumulativePatternsFound = None
        for x in range(-1, 20):
            for y in range(-1, 20):
                patternsFound = self.findPatternAtPosition(x, y, color, pattern, [ Board.East, Board.Southeast, Board.South, Board.Southwest ])
                if patternsFound:
                    if cumulativePatternsFound is None:
                        cumulativePatternsFound = []
                    cumulativePatternsFound += patternsFound
        return cumulativePatternsFound


    def findPatternAtPosition(self, x, y, color, pattern, directions):
        patternsFound = None
        for direction in directions:
            save = self.findPatternAtPositionInDirection(x, y, color, pattern, direction)
            if save:
                if patternsFound is None:
                    patternsFound = []
                patternsFound += [ { 'name': pattern['name'], 'direction': direction['name'], 'positions': save } ]

        return patternsFound


    # Returns:
    # - None if the pattern did not match in the direction
    # - An array of matched positions if the pattern was detected
    #   Note: If there are no detected positions but the patterns was found, then [] is returned
    def findPatternAtPositionInDirection(self, x, y, color, pattern, direction):
        save = []
        for token in pattern['tokens']:
            tokens = token.split(':')
            if not self.expectedTokenAtPosition(x, y, color, tokens[0]):
                return None

            if len(tokens) == 2:
                save.append({ 'x': x, 'y': y })
            elif len(tokens) == 3:
                save.append({ 'x': x, 'y': y, 'weight': tokens[2] })

            # Update the position in the appropriate direction to get ready to look for the next token in the pattern
            x += direction['xOffset']
            y += direction['yOffset']

        # If we made it this far, all the tokens in the pattern were found
        return save


    def expectedTokenAtPosition(self, x, y, color, expectedToken):

        # bead
        #
        # matches a bead played at the position by the current player
        if expectedToken == 'bead':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if self.getBead(x, y) == color:
                return True
            return False

        # opponent
        #
        # matches a bead played at the position by an opposing player
        if expectedToken == 'opponent':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if not self.isOpen(x, y) and self.getBead(x, y) != color:
                return True
            return False

        # open
        #
        # matches a position with no bead
        if expectedToken == 'open':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if self.isOpen(x, y):
                return True
            return False

        # not-bead
        #
        # not-bead means will match anything in the position other
        # than the current player's bead color including:
        # 1. a position that is off the board
        # 2. another player's bead
        # 3. an open position
        if expectedToken == 'not-bead':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return True

            if (self.getBead(x, y) != color):
                return True

            return False

        # closed
        #
        # Matches two scenarios:
        # 1. a position that is off the board
        # 2. a position occupied by an opposing player's bead
        if expectedToken == 'closed':
            if (x > 18 or x < 0 or y > 18 or y < 0):
                return True
            if not self.isOpen(x, y) and self.getBead(x, y) != color:
                return True
            return False

        print('board: we should never get here: expectedToken=' + expectedToken)
        sys.exit(1)


    def __str__(self):
        s = '   '
        for x in range(19):
            s += str(x  % 10) + ' '
        s += '\n'
        for y in range(19):
            s += str(y % 10)  + '  '
            for x in range(19):
                if self.isOpen(x, y):
                    s += '. '
                else:
                    if self.getBeadHighlight(x, y):
                        s += self.getBead(x, y)[0] + ' '
                    else:
                        s += self.getBead(x, y)[0].lower() + ' '
            s += '\n'
        return s
