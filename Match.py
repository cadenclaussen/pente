import random

from Game import Game

class Match:
    players = None
    game = None
    gameCount = -1
    winner = None
    priorLoser = None
    points = {}


    def __init__(self):
        self.players = [ 'Blue', 'Green' ]
        self.gameCount = -1
        self.points[self.players[0]] = 0
        self.points[self.players[1]] = 0


    def newGame(self):
        self.gameCount += 1
        self.game = Game(self, self.players, self.priorLoser if self.priorLoser is not None else random.choice(self.players))


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
