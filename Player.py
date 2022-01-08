class Player:
    def __init__(self, name, color, key):
        self.name = name
        self.color = color
        self.key = key
        self.jumps = 0
        self.score = 0

    def __str__(self):
        s = self.name + " [" + self.color + "]"
        return s
