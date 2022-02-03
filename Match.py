import random

from Game import Game

class Match:
    colors = None
    game = None
    gameCount = 0
    winner = None
    priorLoser = None
    points = {}


    def __init__(self):
        self.colors = [ 'Blue', 'Green' ]
        self.gameCount = -1
        self.points[self.colors[0]] = 0
        self.points[self.colors[1]] = 0


    def newGame(self):
        self.gameCount += 1
        self.game = Game(self, self.colors, self.priorLoser if self.priorLoser is not None else random.choice(self.colors))


    def isWinner(self):
        return self.winner != None


    def __str__(self):
        s = ''
        s += self.game.board.__str__()
        s += 'Match:\n'
        s += '  Game Count: ' + str(self.gameCount) + '\n'
        s += '  Winner: ' + str(self.winner if self.winner is not None else 'None') + '\n'
        s += '  Pior loser: ' + str(self.priorLoser if self.priorLoser is not None else 'None') + '\n'
        for player in self.points.keys():
            s += '  ' + player + ': ' + str(self.points[player]) + '\n'
        s += self.game.__str__()
        return s
