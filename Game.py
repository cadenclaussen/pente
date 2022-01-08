class Game:
    def __init__(self):
        self.beadsPlayed = 0
        self.winner = False


    # This is temporary just to test out the view
    def isWinner(self):
        if self.beadsPlayed == 20:
            self.winner = True
        return self.winner
