from Board import Board


class Game:
    MatchWin = 33
    match = None
    colors = None
    beadsPlayed = 0
    currentColor = None
    opponentColor = None
    winner = None
    board = None
    lastMove = None
    jumps = {}
    points = {}


    def __init__(self, match, colors, startingColor):
        self.match = match
        self.colors = colors
        self.currentColor = startingColor
        if self.currentColor == self.colors[0]:
            self.opponentColor = self.colors[1]
        else:
            self.opponentColor = self.colors[0]
        self.board = Board(colors)
        for color in colors:
            self.jumps[color] = 0
            self.points[color] = 0


    def nextColor(self):
        self.opponentColor = self.currentColor
        if self.currentColor == self.colors[0]:
            self.currentColor = self.colors[1]
        else:
            self.currentColor = self.colors[0]


    def addJumps(self, color, count):
        self.jumps[color] += count


    def setPoints(self, color, count):
        self.points[color] = count


    def addBead(self, x, y):
        self.lastMove = { 'x': x, 'y': y }
        self.beadsPlayed += 1
        self.board.addBead(x, y, self.currentColor)
        self.nextColor()
        self.postMove()


    # TODO: More to do here, undo jumps, keep move from two moves ago, revamp score
    def undoLastMove(self):
        self.beadsPlayed -= 1
        self.board.removeBead(self.lastMove['x'], self.lastMove['y'])
        self.nextColor()
        self.postMove()


    def postMove(self):
        print(str(self.jumps))

        # Find every known pattern on the board for the color and opponent
        self.board.analyze(self.currentColor, self.opponentColor, self.lastMove)

        # Re-init points, this function will re-calcuate the points...
        self.points[self.opponentColor] = self.jumps[self.opponentColor]
        self.points[self.currentColor] = self.jumps[self.currentColor]

        # If the opponent's last move resulted in 1+ jumps...
        if len(self.board.getOpponentJumps()) > 0:
            self.jumps[self.opponentColor] += int(len(self.board.getOpponentJumps()) / 2)
            self.points[self.opponentColor] += int(len(self.board.getOpponentJumps()) / 2)
            if self.jumps[self.opponentColor] >= 5:
                self.winner = self.opponentColor

        # If the opponent's last move resulted in 5+ bead sequence...
        if self.board.getWinner(self.opponentColor):
            self.points[self.opponentColor] += 5
            self.winner = self.opponentColor

        # Add any points found as a result of analyzing the board
        self.points[self.opponentColor] += self.board.getPoints(self.opponentColor)
        self.points[self.currentColor] += self.board.getPoints(self.currentColor)

        if self.winner is not None:
            self.match.points[self.opponentColor] += self.points[self.opponentColor]
            self.match.points[self.currentColor] += self.points[self.currentColor]
            if self.match.points[self.opponentColor] > self.MatchWin:
                self.match.winner = self.opponentColor
                self.match.priorLoser = self.currentColor
            elif self.match.points[self.currentColor] > self.MatchWin:
                self.match.winner = self.currentColor
                self.match.priorLoser = self.opponentColor


    def isWinner(self):
        return self.winner != None


    def __str__(self):
        s = 'Game:\n'
        s += '  Last move: ' + str(self.lastMove) + '\n'
        s += '  Winner: ' + str(self.winner if (self.winner is not None) else 'None') + '\n'
        s += '  Beads Played: ' + str(self.beadsPlayed) + '\n'
        s += '  Current color: ' + self.currentColor + '\n'
        return s
