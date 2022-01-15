import sys


class Board:
    East = { "name": "east", "rowOffset": 0, "columnOffset": 1 }
    Southeast = { "name": "southeast", "rowOffset": 1, "columnOffset": 1 }
    South = { "name": "south", "rowOffset": 1, "columnOffset": 0 }
    Southwest = { "name": "southwest", "rowOffset": 1, "columnOffset": -1 }
    West = { "name": "west", "rowOffset": 0, "columnOffset": -1 }
    Northwest = { "name": "northwest", "rowOffset": -1, "columnOffset": -1 }
    North = { "name": "north", "rowOffset": -1, "columnOffset": 0 }
    Northeast = { "name": "northeast", "rowOffset": -1, "columnOffset": 1 }


    def __init__(self):
        self.jumpPatterns = []
        self.winningPatterns = []
        self.announcePatterns = { 'Shane': [], 'Caden': [] }
        self.pointPatterns = { 'Shane': [], 'Caden': [] }
        self.board = []
        for row in range(19):
            self.board.append([])
            for column in range(19):
                self.board[row].append(".")


    def removeFromBoard(self, position):
        self.board[position["column"]][position["row"]] = "."


    def playBead(self, currentPlayer, position):
        self.board[position["column"]][position["row"]] = currentPlayer.color[0]


    # TODO: If there are three players this needs to be updated so the two opponent beads are the same bead
    def findJumpPatterns(self, currentPlayer, position):
        self.jumpPatterns = []

        patterns = []
        patterns.append({ "name": "Jump", "tokens": [ "bead", "opponent", "opponent", "bead" ]})

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPatternAtPosition(currentPlayer, patterns[0], position, [ Board.East, Board.Southeast, Board.South, Board.Southwest, Board.West, Board.Northwest, Board.North, Board.Northeast ], "opponent")
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.jumpPatterns = cumulativePatternsFound
        for jumpPattern in self.jumpPatterns:
            for position in jumpPattern["positions"]:
                self.removeFromBoard(position)

        return self.jumpPatterns != []


    def findWinningPatterns(self, currentPlayer):
        self.winningPatterns = []

        patterns = []
        patterns.append({ "name": "Five", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Six", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Seven", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Eight", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Nine", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, "bead")
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.winningPatterns = cumulativePatternsFound
        return self.winningPatterns != []


    def findAnnouncePatterns(self, currentPlayer):
        self.announcePatterns[currentPlayer.name] = []

        patterns = []
        patterns.append({ "name": "Open Three", "tokens": [ "not-bead", "open", "bead", "bead", "bead", "open", "not-bead" ] })
        patterns.append({ "name": "Holed Open Four", "tokens": [ "open", "bead", "open", "bead", "bead", "open" ] })
        patterns.append({ "name": "Holed Open Four", "tokens": [ "open", "bead", "bead", "open", "bead", "open" ] })
        patterns.append({ "name": "Closed Four", "tokens": [ "open", "bead", "bead", "bead", "bead", "closed" ] })
        patterns.append({ "name": "Closed Four", "tokens": [ "closed", "bead", "bead", "bead", "bead", "open" ] })
        patterns.append({ "name": "Open Four", "tokens": [ "open", "bead", "bead", "bead", "bead", "open" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "open", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "bead", "open", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "bead", "bead", "open", "bead", "not-bead" ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, "bead")
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.announcePatterns[currentPlayer.name] = cumulativePatternsFound
        return self.announcePatterns[currentPlayer.name] != []


    # TODO: Include all the winning pattern variants as well
    def findPointPatterns(self, currentPlayer):
        self.pointPatterns[currentPlayer.name] = []

        patterns = []
        patterns.append({ "name": "Four", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Five", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Six", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Seven", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Eight", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Nine", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })

        cumulativePatternsFound = []
        for pattern in patterns:
            patternsFound = self.__findPattern(currentPlayer, pattern, "bead")
            if patternsFound:
                cumulativePatternsFound += patternsFound

        self.pointPatterns[currentPlayer.name] = cumulativePatternsFound

        return self.pointPatterns[currentPlayer.name] != []


    def __findPattern(self, currentPlayer, pattern, tokenNameToSavePositionFor):
        cumulativePatternsFound = None
        for row in range(-1, 20):
            for column in range(-1, 20):
                patternsFound = self.__findPatternAtPosition(currentPlayer, pattern, { "row": row, "column": column }, [ Board.East, Board.Southeast, Board.South, Board.Southwest ], tokenNameToSavePositionFor)
                if patternsFound:
                    if cumulativePatternsFound is None:
                        cumulativePatternsFound = []
                    cumulativePatternsFound += patternsFound
        return cumulativePatternsFound


    def __findPatternAtPosition(self, currentPlayer, pattern, position, directions, tokenNameToSavePositionFor):
        patternsFound = None
        for direction in directions:
            positionsFound = self.__findPatternAtPositionInDirection(currentPlayer, pattern, position, direction, tokenNameToSavePositionFor)
            if positionsFound:
                if patternsFound is None:
                    patternsFound = []
                patternsFound += [ { "name": pattern["name"], "direction": direction["name"], "positions": positionsFound } ]

        return patternsFound


    # Returns:
    # - None if the pattern did not match in the direction
    # - An array of matched positions if the pattern was detected
    #   Note: If there are no detected positions but the patterns was found, then [] is returned
    def __findPatternAtPositionInDirection(self, currentPlayer, pattern, position, direction, tokenNameToSavePositionFor):
        positionsFound = []
        for token in pattern["tokens"]:
            if not self.expectedTokenAtPosition(currentPlayer, position, token):
                return None

            if token == tokenNameToSavePositionFor:
                positionsFound.append({ "row": position["row"], "column": position["column"] })

            # Update the position in the appropriate direction to get ready to look for the next token in the pattern
            position = { "row": (position["row"] + direction["rowOffset"]), "column": (position["column"] + direction["columnOffset"])}

        # If we made it this far, all the tokens in the pattern were
        return positionsFound


    def expectedTokenAtPosition(self, currentPlayer, position, token):
        row = position["row"]
        column = position["column"]

        # bead
        #
        # matches a bead played at the position by the current player
        if token == "bead":
            if row > 18 or row < 0 or column > 18 or column < 0:
                return False
            if self.board[column][row] == currentPlayer.color[0]:
                return True
            return False

        # opponent
        #
        # matches a bead played at the position by an opposing player
        if token == "opponent":
            if row > 18 or row < 0 or column > 18 or column < 0:
                return False
            if self.board[column][row] != '.' and self.board[column][row] != currentPlayer.color[0]:
                return True
            return False

        # open
        #
        # matches a position with no bead
        if token == "open":
            if row > 18 or row < 0 or column > 18 or column < 0:
                return False
            if self.board[column][row] == '.':
                return True
            return False

        # not-bead
        #
        # not-bead means will match anything in the position other
        # than the current player's bead color including:
        # 1. a position that is off the board
        # 2. another player's bead
        # 3. an open position
        if token == "not-bead":
            if row > 18 or row < 0 or column > 18 or column < 0:
                return True
            if self.board[column][row] != '.' and self.board[column][row] != currentPlayer.color[0]:
                return True
            if self.board[column][row] == ".":
                return True
            return False

        # closed
        #
        # Matches two scenarios:
        # 1. a position that is off the board
        # 2. a position occupied by an opposing player's bead
        if token == "closed":
            if (row > 18 or row < 0 or column > 18 or column < 0):
                return True
            if self.board[column][row] != '.' and self.board[column][row] != currentPlayer.color[0]:
                return True
            return False

        print('board: we should never get here: token=' + token)
        sys.exit(1)


    def __str__(self):
        s = "   "
        for column in range(19):
            s += str(column  % 10) + " "
        s += "\n"
        for row in range(19):
            s += str(row % 10)  + "  "
            for column in range(19):
                s += str(self.board[column][row]) + " "
            s += "\n"
        return s
