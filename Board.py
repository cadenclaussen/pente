import sys

class Board:
    def __init__(self):
        self.board = []
        for row in range(19):
            self.board.append([])
            for col in range(19):
                self.board[row].append(".")

    def playBead(self, currentPlayer, position):
        self.board[position["col"]][position["row"]] = currentPlayer.color[0];


    def findWinningPatterns(self, currentPlayer):
        patterns = []
        patterns.append({ "name": "Five", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Six", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Seven", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Eight", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Nine", "tokens": [ "not-bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "bead", "not-bead" ] })

        patternsFound = []
        for pattern in patterns:
            self.findPattern(currentPlayer, pattern, patternsFound)

        return patternsFound


    # TODO: If there are three players this needs to be updated so the two opponent beads are the same bead
    def findJumpPatterns(self, currentPlayer, position):
        patterns = []
        patterns.append({ "name": "Jump", "tokens": [ "bead", "opponent", "opponent", "bead" ]})
        # TODO: Update this so the jump is checked in all directions, two options:
        # 1: Change findPatternAtPosition to take an option to determine which direction set to use
        # 2: Change this code to call findPatternAtPositionInDirection for all 8 directions
        patternsFound = []
        for pattern in patterns:
            self.findPatternAtPosition(currentPlayer, pattern, position, patternsFound, True)

        return patternsFound


    def findPatternsToAnnounce(self, currentPlayer):
        patterns = []
        patterns.append({ "name": "Open Three", "tokens": [ "open", "bead", "bead", "bead", "open" ] })
        patterns.append({ "name": "Open Four", "tokens": [ "open", "bead", "bead", "bead", "bead", "open" ] })
        patterns.append({ "name": "Holed Open Four", "tokens": [ "open", "bead", "open", "bead", "bead", "open" ] })
        patterns.append({ "name": "Holed Open Four", "tokens": [ "open", "bead", "bead", "open", "bead", "open" ] })
        patterns.append({ "name": "Closed Four", "tokens": [ "open", "bead", "bead", "bead", "bead", "closed" ] })
        patterns.append({ "name": "Closed Four", "tokens": [ "closed", "bead", "bead", "bead", "bead", "open" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "open", "bead", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "bead", "open", "bead", "bead", "not-bead" ] })
        patterns.append({ "name": "Holed Five", "tokens": [ "not-bead", "bead", "bead", "bead", "open", "bead", "not-bead" ] })
        # TODO: Add the variations for holed 6, 7, 8, and 9 as well

        patternsFound = []
        for pattern in patterns:
            self.findPattern(currentPlayer, pattern, patternsFound)

        return patternsFound


    # TODO: Implement
    def findScorePatterns(self, currentPlayer):
        pass

    def findPattern(self, currentPlayer, pattern, patternsFound):
        for row in range(19):
            for col in range(19):
                self.findPatternAtPosition(currentPlayer, pattern, { "row": row, "col": col }, patternsFound, False)


    def findPatternAtPosition(self, currentPlayer, pattern, position, patternsFound, full):
        directions = []
        directions.append({ "name": "east", "rowDelta": 0, "colDelta": 1 })
        directions.append({ "name": "southeast", "rowDelta": 1, "colDelta": 1 })
        directions.append({ "name": "south", "rowDelta": 1, "colDelta": 0 })
        directions.append({ "name": "southwest", "rowDelta": 1, "colDelta": -1 })

        if (full):
            directions.append({ "name": "west", "rowDelta": 0, "colDelta": -1 })
            directions.append({ "name": "northwest", "rowDelta": -1, "colDelta": 1 })
            directions.append({ "name": "north", "rowDelta": 0, "colDelta": 1 })
            directions.append({ "name": "northeast", "rowDelta": -1, "colDelta": 1 })

        for direction in directions:
            if self.findPatternAtPositionInDirection(currentPlayer, pattern, position, direction):
                patternsFound.append({ "name": pattern["name"], "direction": direction["name"], "position": position })
                print('Pattern: ' + str(currentPlayer) + " " + pattern["name"] + " @ [" + str(position["col"]) + "," + str(position["row"]) + "] in the " + direction["name"] + " direction")


    def findPatternAtPositionInDirection(self, currentPlayer, pattern, position, direction):
        for token in pattern["tokens"]:
            if not self.expectedTokenAtPosition(currentPlayer, position, token):
                return False

            # Update the position to check for the next expected token
            position = { "row": (position["row"] + direction["rowDelta"]), "col": (position["col"] + direction["colDelta"])}

        # If we made it this far, all the tokens in the pattern were
        # found, so the pattern we were searching for was detected
        return True


    def expectedTokenAtPosition(self, currentPlayer, position, token):
        row = position["row"]
        col = position["col"]

        # bead
        #
        # matches a bead played at the position by the current player
        if token == "bead":
            if row > 18 or row < 0 or col > 18 or col < 0:
                return False
            if self.board[col][row] == currentPlayer.color[0]:
                return True
            return False

        # opponent
        #
        # matches a bead played at the position by an opposing player
        if token == "opponent":
            if row > 18 or row < 0 or col > 18 or col < 0:
                return False
            if self.board[col][row] != '.' and self.board[col][row] != currentPlayer.color[0]:
                return True
            return False

        # open
        #
        # matches a position with no bead
        if token == "open":
            if row > 18 or row < 0 or col > 18 or col < 0:
                return False
            if self.board[col][row] == '.':
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
            if row > 18 or row < 0 or col > 18 or col < 0:
                return True
            if self.board[col][row] != '.' and self.board[col][row] != currentPlayer.color[0]:
                return True
            if self.board[col][row] == ".":
                return True
            return False

        # closed
        #
        # Matches two scenarios:
        # 1. a position that is off the board
        # 2. a position occupied by an opposing player's bead
        if token == "closed":
            if (row > 18 or row < 0 or col > 18 or col < 0):
                return True
            if self.board[col][row] != '.' and self.board[col][row] != currentPlayer.color[0]:
                return True
            return False

        print('board: we should never get here: token=' + token)
        sys.exit(1)


    def __str__(self):
        s = "   "
        for col in range(19):
            s += str(col  % 10) + "  "
        s += "\n"
        for row in range(19):
            s += str(row % 10)  + "  "
            for col in range(19):
                s += str(self.board[col][row]) + "  "
            s += "\n"
        return s
