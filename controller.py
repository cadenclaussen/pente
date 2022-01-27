import random
from Player import Player
from Match import Match
from Board import Board


match = None
board = None
players = None
currentPlayer = None


def newMatch():
    global match, board, players, currentPlayer
    match = Match()
    players = [ Player('Shane', 'Blue', 0), Player('Caden', 'Green', 1) ]
    return [ match, board, players, currentPlayer ]


def newGame():
    global match, board, players, currentPlayer
    board = Board(players)
    if match.losingPlayer is None:
        currentPlayer = random.choice(players)
    else:
        currentPlayer = match.losingPlayer
    match.newGame()

    printDebug()
    return [ match, board, players, currentPlayer ]


def playBead(x, y):
    global match, board, players, currentPlayer

    # Algorithm upon placing a bead:
    # - Put the bead on the board object
    # - Jumps: If the move result in jump(s), save them, adjust game points, and set game winner if > 5
    # - Winning Patterns: If the move resulted in winning pattern(s), adjust game points and set game winner
    # - Point Patterns: Find all point patterns as a result of the move, adjust points
    # - Announce Patterns: Find all announce patterns as a result of the move, save them
    # - Match Win: If there was a game win, determine if it caused a match win, if so set match winner
    #
    # - Change to the next player
    # - Point Patterns: Find all point patterns as a result of the move, adjust points
    # - Announce Patterns: Find all announce patterns as a result of the move, save them
    board.playBead(x, y, currentPlayer.color)
    match.beadsPlayed += 1

    currentPlayer.gamePoints = 0
    if board.findJumpPatterns(x, y, currentPlayer.color):
        currentPlayer.jumps += len(board.jumpPatterns)
        if currentPlayer.jumps >= 5:
            match.gameWinner = True
    currentPlayer.gamePoints += currentPlayer.jumps

    if board.findWinningPatterns(currentPlayer.color):
        currentPlayer.gamePoints += 5
        match.gameWinner = True

    if board.findPointPatterns(currentPlayer.color):
        currentPlayer.gamePoints += len(board.pointPatterns[currentPlayer.color])

    board.findAnnouncePatterns(currentPlayer.color)

    if match.isGameWinner():
        currentPlayer.matchPoints += currentPlayer.gamePoints
        currentPlayer.gamePoints = 0
        currentPlayer.jumps = 0
        if currentPlayer.matchPoints > Match.MatchWin:
            match.matchWinner = True


    nextPlayer()


    currentPlayer.gamePoints = 0
    currentPlayer.gamePoints += currentPlayer.jumps
    if board.findPointPatterns(currentPlayer.color):
        currentPlayer.gamePoints += len(board.pointPatterns[currentPlayer.color])

    board.findAnnouncePatterns(currentPlayer.color)

    board.findOffensePatterns(currentPlayer.color)

    if match.isGameWinner():
        currentPlayer.matchPoints += currentPlayer.gamePoints
        currentPlayer.gamePoints = 0
        currentPlayer.jumps = 0
        match.losingPlayer = currentPlayer


    printDebug()
    return match, board, players, currentPlayer


def printDebug():
    global game, board, players, currentPlayer
    print(board)
    print()
    printPlayer(players[0])
    printPlayer(players[1])
    print()
    print('Game Count: ' + str(match.gameCount))
    print('Game Winner: ' + str(match.isGameWinner()))
    print('Match Winner: ' + str(match.isMatchWinner()))
    print()
    print('Next Move: ' + currentPlayer.name)


def printPlayer(player):
    print(player.name)
    print('------------------------------')
    print('Jumps: ' + str(player.jumps))
    print('Match points: ' + str(player.matchPoints))
    print('Game points: ' + str(player.gamePoints))

    if board.pointPatterns[player.color] != []:
        print('Point patterns: ')
        for pointPattern in board.pointPatterns[player.color]:
            print('  ' + pointPattern['name'] + positions(pointPattern['positions']))

    if board.announcePatterns[player.color] != []:
        print('Announce patterns: ')
        for announcePattern in board.announcePatterns[player.color]:
            print('  ' + announcePattern['name'] + positions(announcePattern['positions']))

    if board.offensePatterns[player.color] != []:
        print('Offense patterns: ')
        for offensePattern in board.offensePatterns[player.color]:
            print('  ' + offensePattern['name'] + positions(offensePattern['positions']))

    print()


def positions(positions):
    s = ''
    for position in positions:
        s += ' (' + str(position['x']) + ',' + str(position['y']) + ')'
    return s


def nextPlayer():
    global game, board, players, currentPlayer
    if currentPlayer.key == 0:
        currentPlayer = players[1]
    else:
        currentPlayer = players[0]
