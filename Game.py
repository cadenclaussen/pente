class Game:
    beadsPlayed = None

    def __init__(self):
        self.beadsPlayed = 0

    # This is temporary just to test out the view
    def isWinner(self):
        if self.beadsPlayed == 4:
            return True
        return False
