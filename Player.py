class Player:
    key = None
    name = None
    color = None
    matchPoints = 0
    jumps = 0
    points = 0


    def __init__(self, name, color, key):
        self.key = key
        self.name = name
        self.color = color
        self.jumps = 0
        self.points = 0
        self.matchPoints = 0


    def __str__(self):
        s = self.name + ' [' + self.color + ']\n'
        s += '  Jumps: ' + str(self.jumps) + '\n'
        s += '  Points: ' + str(self.points) + '\n'
        s += '  Match Points: ' + str(self.matchPoints) + '\n'
        return s
