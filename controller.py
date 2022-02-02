from Match import Match


match = None


def newMatch():
    print('Entering: newMatch')
    global match, game
    match = Match()
    return match


def newGame():
    print('Entering: newGame')
    global match
    match.newGame()
    print(match)
    return match


def addBead(x, y):
    print('Entering: addBead')
    global match
    match.game.addBead(x, y)
    print(match)
    return match


def undoLastMove(x, y):
    print('Entering: undoLastMove')
    global match
    match.game.undoLastMove(x, y)
    print(match)
    return match
