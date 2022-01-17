class Match:
    def __init__(self):
        self.gameCount = 0
        self.beadsPlayed = 0
        self.gameWinner = False
        self.matchWinner = False
        self.losingPlayer = None


    def newGame(self):
        self.beadsPlayed = 0
        self.gameWinner = False
        self.matchWinner = False
        self.gameCount += 1


    def isGameWinner(self):
        return self.gameWinner


    def isMatchWinner(self):
        return self.matchWinner
