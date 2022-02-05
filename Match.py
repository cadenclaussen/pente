import random
from Game import Game
from Status import Status


class Match:
    MatchWin = 7

    colors = None
    game = None
    gameCount = 0
    winner = None
    priorGameLoser = None
    status = None
    points = {}


    def __init__(self):
        self.colors = [ 'Blue', 'Red' ]
        self.gameCount = -1
        self.points[self.colors[0]] = 0
        self.points[self.colors[1]] = 0
        self.status = Status.PreMatch


    def newGame(self):
        self.gameCount += 1
        self.game = Game(self, self.colors, self.priorGameLoser if self.priorGameLoser is not None else random.choice(self.colors))
        self.status = Status.InProgress


    def updateMatchScore(self, winner, winnerGamePoints, loser, loserGamePoints):
        self.priorGameLoser = loser

        self.points[winner] += winnerGamePoints
        self.points[loser] += loserGamePoints

        if self.points[winner] > self.MatchWin:
            self.setWinner(winner)
        elif self.points[loser] > self.MatchWin:
            self.setWinner(loser)


    def setWinner(self, winner):
        self.winner = winner
        self.status = Status.Finished


    def isWinner(self):
        return self.status == Status.Finished


    def __str__(self):
        s = ''
        s += self.game.board.__str__()
        s += 'Match:\n'
        s += '  Game Count: ' + str(self.gameCount) + '\n'
        s += '  Winner: ' + str(self.winner if self.winner is not None else 'None') + '\n'
        s += '  Prior game loser: ' + str(self.priorGameLoser if self.priorGameLoser is not None else 'None') + '\n'
        for color in self.points.keys():
            s += '  ' + color + ': ' + str(self.points[color]) + '\n'
        s += self.game.__str__()
        return s
