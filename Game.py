from Board import Board
from Status import Status


class Game:
    match = None
    colors = None
    beadsPlayed = 0
    currentColor = None
    opponentColor = None
    winner = None
    loser = None
    board = None
    lastMove = None
    jumps = {}
    points = {}
    status = None


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
        self.status = Status.InProgress


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


    def postMove(self):

        # Find every known pattern on the board for the color and opponent
        self.board.analyze(self.currentColor, self.opponentColor, self.lastMove, self.beadsPlayed)

        # Re-init points, this function will re-calcuate the points...
        self.points[self.opponentColor] = self.jumps[self.opponentColor]
        self.points[self.currentColor] = self.jumps[self.currentColor]

        # If the opponent's last move resulted in 1+ jumps...
        if len(self.board.getOpponentJumps()) > 0:
            self.jumps[self.opponentColor] += int(len(self.board.getOpponentJumps()) / 2)
            self.points[self.opponentColor] += int(len(self.board.getOpponentJumps()) / 2)
            if self.jumps[self.opponentColor] >= 5:
                self.setWinner(self.opponentColor, self.currentColor)

        # If the opponent's last move resulted in 5+ bead sequence...
        if self.board.getWinner(self.opponentColor):
            self.points[self.opponentColor] += 5
            self.setWinner(self.opponentColor, self.currentColor)

        # Add any points found as a result of analyzing the board
        self.points[self.opponentColor] += self.board.getPoints(self.opponentColor)
        self.points[self.currentColor] += self.board.getPoints(self.currentColor)

        if self.isWinner():
            self.match.updateMatchScore(self.winner, self.points[self.winner], self.loser, self.points[self.loser])


    def setWinner(self, winner, loser):
        self.winner = winner
        self.loser = loser
        self.status = Status.Finished


    def isWinner(self):
        return self.status == Status.Finished


    def __str__(self):
        s = 'Game:\n'
        s += '  Last move: ' + str(self.lastMove) + '\n'
        s += '  Winner: ' + str(self.winner if (self.winner is not None) else 'None') + '\n'
        s += '  Beads Played: ' + str(self.beadsPlayed) + '\n'
        s += '  Current color: ' + self.currentColor + '\n'
        return s
