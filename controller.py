from Match import Match


match = None


def newMatch():
    global match, game
    match = Match()
    return match


def newGame():
    global match
    match.newGame()
    print(match)
    return match


def addBead(x, y):
    global match
    match.game.addBead(x, y)
    print(match)
    return match


def undoLastMove(x, y):
    global match
    match.game.undoLastMove(x, y)
    print(match)
    return match
