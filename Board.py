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


    def __init__(self):
        self.jumpPatterns = []
        self.winningPatterns = []
        self.announcePatterns = { 'Shane': [], 'Caden': [] }
        self.pointPatterns = { 'Shane': [], 'Caden': [] }

        self.board = []
        for y in range(19):
            self.board.append([])
            for x in range(19):
                self.board[y].append({ 'bead': 'Open', 'highlight': False, 'weight': 0 })


    def playBead(self, x, y, color):
        self.board[y][x]['bead'] = color


    def removeBead(self, x, y):
        self.board[y][x]['bead'] = 'Open'


    # TODO: Use a consistent position or y/x model
    def getBead(self, x, y):
        return self.board[y][x]['bead']


    # TODO: Use a consistent position or y/x model
    def isOpen(self, x, y):
        return (self.board[y][x]['bead'] == 'Open')


    # TODO: If there are three players this needs to be updated so the two opponent beads are the same bead
    def findJumpPatterns(self, currentPlayer, x, y):
        self.jumpPatterns = []

        patterns = []
        patterns.append({ 'name': 'Jump', 'tokens': [ 'bead', 'opponent', 'opponent', 'bead' ]})

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPatternAtPosition(currentPlayer, patterns[0], x, y, [ Board.East, Board.Southeast, Board.South, Board.Southwest, Board.West, Board.Northwest, Board.North, Board.Northeast ], 'opponent')
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.jumpPatterns = cumulativePatternsFound
        for jumpPattern in self.jumpPatterns:
            for position in jumpPattern['positions']:
                self.removeBead(position['x'], position['y'])

        return self.jumpPatterns != []


    def findWinningPatterns(self, currentPlayer):
        self.winningPatterns = []

        patterns = []
        patterns.append({ 'name': 'Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Six', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Seven', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Eight', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Nine', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, 'bead')
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.winningPatterns = cumulativePatternsFound
        return self.winningPatterns != []


    def findAnnouncePatterns(self, currentPlayer):
        self.announcePatterns[currentPlayer.name] = []

        patterns = []
        patterns.append({ 'name': 'Open Three', 'tokens': [ 'not-bead', 'open', 'bead', 'bead', 'bead', 'open', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'open', 'bead', 'open', 'bead', 'bead', 'open' ] })
        patterns.append({ 'name': 'Holed Open Four', 'tokens': [ 'open', 'bead', 'bead', 'open', 'bead', 'open' ] })
        patterns.append({ 'name': 'Closed Four', 'tokens': [ 'open', 'bead', 'bead', 'bead', 'bead', 'closed' ] })
        patterns.append({ 'name': 'Closed Four', 'tokens': [ 'closed', 'bead', 'bead', 'bead', 'bead', 'open' ] })
        patterns.append({ 'name': 'Open Four', 'tokens': [ 'open', 'bead', 'bead', 'bead', 'bead', 'open' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'open', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'open', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Holed Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'open', 'bead', 'not-bead' ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, 'bead')
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.announcePatterns[currentPlayer.name] = cumulativePatternsFound
        return self.announcePatterns[currentPlayer.name] != []


    # TODO: Resolve the issue of a win ...
    def findPointPatterns(self, currentPlayer):
        self.pointPatterns[currentPlayer.name] = []

        patterns = []
        patterns.append({ 'name': 'Four', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Five', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Six', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Seven', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Eight', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })
        patterns.append({ 'name': 'Nine', 'tokens': [ 'not-bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'bead', 'not-bead' ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, 'bead')
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.pointPatterns[currentPlayer.name] = cumulativePatternsFound

        return self.pointPatterns[currentPlayer.name] != []


    def __findPattern(self, currentPlayer, pattern, tokenNameToSavePositionFor):
        cumulativePatternsFound = None
        for x in range(-1, 20):
            for y in range(-1, 20):
                patternsFound = self.__findPatternAtPosition(currentPlayer, pattern, x, y, [ Board.East, Board.Southeast, Board.South, Board.Southwest ], tokenNameToSavePositionFor)
                if patternsFound:
                    if cumulativePatternsFound is None:
                        cumulativePatternsFound = []
                    cumulativePatternsFound += patternsFound
        return cumulativePatternsFound


    def __findPatternAtPosition(self, currentPlayer, pattern, x, y, directions, tokenNameToSavePositionFor):
        patternsFound = None
        for direction in directions:
            positionsFound = self.findPatternAtPositionInDirection(currentPlayer, pattern, x, y, direction, tokenNameToSavePositionFor)
            if positionsFound:
                if patternsFound is None:
                    patternsFound = []
                patternsFound += [ { 'name': pattern['name'], 'direction': direction['name'], 'positions': positionsFound } ]

        return patternsFound


    # Returns:
    # - None if the pattern did not match in the direction
    # - An array of matched positions if the pattern was detected
    #   Note: If there are no detected positions but the patterns was found, then [] is returned
    def findPatternAtPositionInDirection(self, currentPlayer, pattern, x, y, direction, tokenNameToSavePositionFor):
        positionsFound = []
        for token in pattern['tokens']:
            if not self.__expectedTokenAtPosition(currentPlayer, x, y, token):
                # print('RETURNING')
                # print()
                return None

            if token == tokenNameToSavePositionFor:
                positionsFound.append({ 'x': x, 'y': y })

            # Update the position in the appropriate direction to get ready to look for the next token in the pattern
            x += direction['xOffset']
            y += direction['yOffset']

        # If we made it this far, all the tokens in the pattern were found
        # print('Found pattern at position in direction')
        # print()
        return positionsFound


    def __expectedTokenAtPosition(self, currentPlayer, x, y, token):

        # bead
        #
        # matches a bead played at the position by the current player
        if token == 'bead':
            # print('Looking for bead ' + str(x) + ' ' + str(y))
            if x > 18 or x < 0 or y > 18 or y < 0:
                # print('  NOT found (out of bounds)')
                return False
            if self.getBead(x, y) == currentPlayer.color:
                # print('  Found')
                return True
            # print('  NOT found (was not the players bead)')
            return False

        # opponent
        #
        # matches a bead played at the position by an opposing player
        if token == 'opponent':
            if x > 18 or x < 0 or y > 18 or y < 0:
                return False
            if not self.isOpen(x, y) and self.getBead(x, y) != currentPlayer.color:
                return True
            return False

        # open
        #
        # matches a position with no bead
        if token == 'open':
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
        if token == 'not-bead':
            # print('Looking for not-bead ' + str(x) + ' ' + str(y))
            if x > 18 or x < 0 or y > 18 or y < 0:
                # print('  Found (out of bounds)')
                return True

            if (self.getBead(x, y) != currentPlayer.color):
                # print('  Found (not players bead)')
                return True

            # if (not self.isOpen(x, y)) and self.getBead(x, y) != currentPlayer.color:
            #     return True
            # if self.isOpen(x, y):
            #     return True
            # print('  NOT Found')
            return False

        # closed
        #
        # Matches two scenarios:
        # 1. a position that is off the board
        # 2. a position occupied by an opposing player's bead
        if token == 'closed':
            if (x > 18 or x < 0 or y > 18 or y < 0):
                return True
            if not self.isOpen(x, y) and self.getBead(x, y) != currentPlayer.color:
                return True
            return False

        print('board: we should never get here: token=' + token)
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
                    s += self.getBead(x, y)[0] + ' '
            s += '\n'
        return s
