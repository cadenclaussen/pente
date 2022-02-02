from Board import Board


class Game:
    MatchWin = 33
    match = None
    players = None
    beadsPlayed = 0
    currentPlayer = None
    opponentPlayer = None
    winner = None
    board = None
    lastMove = None
    jumps = {}
    points = {}


    def __init__(self, match, players, startingPlayer):
        self.match = match
        self.players = players
        self.currentPlayer = startingPlayer
        if self.currentPlayer == self.players[0]:
            self.opponentPlayer = self.players[1]
        else:
            self.opponentPlayer = self.players[0]
        self.board = Board(players)
        for player in players:
            self.jumps[player] = 0
            self.points[player] = 0


    def nextPlayer(self):
        self.opponentPlayer = self.currentPlayer
        if self.currentPlayer == self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]


    def addJumps(self, player, count):
        self.jumps[player] += count


    def setPoints(self, player, count):
        self.points[player] = count


    def addBead(self, x, y):
        self.lastMove = { 'x': x, 'y': y }
        self.beadsPlayed += 1
        self.board.addBead(x, y, self.currentPlayer)
        self.nextPlayer()
        self.postMove()


    # TODO: More to do here, undo jumps, keep move from two moves ago, revamp score
    def undoLastMove(self):
        self.beadsPlayed -= 1
        self.board.removeBead(self.lastMove['x'], self.lastMove['y'])
        self.nextPlayer()
        self.postMove()


    def postMove(self):
        print(str(self.jumps))

        # Find every known pattern on the board for the player and opponent
        self.board.analyze(self.currentPlayer, self.opponentPlayer, self.lastMove)

        # Re-init points, this function will re-calcuate the points...
        self.points[self.opponentPlayer] = self.jumps[self.opponentPlayer]
        self.points[self.currentPlayer] = self.jumps[self.currentPlayer]

        # If the opponent's last move resulted in 1+ jumps...
        if len(self.board.getOpponentJumps()) > 0:
            self.jumps[self.opponentPlayer] += int(len(self.board.getOpponentJumps()) / 2)
            self.points[self.opponentPlayer] += int(len(self.board.getOpponentJumps()) / 2)
            if self.jumps[self.opponentPlayer] >= 5:
                self.winner = self.opponentPlayer

        # If the opponent's last move resulted in 5+ bead sequence...
        if self.board.getWinner(self.opponentPlayer):
            self.points[self.opponentPlayer] += 5
            self.winner = self.opponentPlayer

        # Add any points found as a result of analyzing the board
        self.points[self.opponentPlayer] += self.board.getPoints(self.opponentPlayer)
        self.points[self.currentPlayer] += self.board.getPoints(self.currentPlayer)

        if self.winner is not None:
            self.match.points[self.opponentPlayer] += self.points[self.opponentPlayer]
            self.match.points[self.currentPlayer] += self.points[self.currentPlayer]
            if self.match.points[self.opponentPlayer] > self.MatchWin:
                self.match.winner = self.opponentPlayer
                self.match.priorLoser = self.currentPlayer
            elif self.match.points[self.currentPlayer] > self.MatchWin:
                self.match.winner = self.currentPlayer
                self.match.priorLoser = self.opponentPlayer


    def isWinner(self):
        return self.winner != None


    def __str__(self):
        s = 'Game:\n'
        s += '  Last move: ' + str(self.lastMove) + '\n'
        s += '  Winner: ' + str(self.winner if (self.winner is not None) else 'None') + '\n'
        s += '  Beads Played: ' + str(self.beadsPlayed) + '\n'
        s += '  Current player: ' + self.currentPlayer + '\n'
        return s
