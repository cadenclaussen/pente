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

    board.addBead(x, y, currentPlayer.color)
    opponentPlayer = currentPlayer
    match.beadsPlayed += 1
    nextPlayer()

    board.findAllPatternsAllPositionsAllDirections(currentPlayer, currentPlayer.color, opponentPlayer.color, { 'x': x, 'y': y })

    p(opponentPlayer)
    p(currentPlayer)

    for player in [ opponentPlayer, currentPlayer ]:

        player.gamePoints = 0

        if len(board.jumps) > 0:
            player.jumps += len(board.jumps)
            player.gamePoints += player.jumps
            if player.jumps >= 5:
                match.gameWinner = True

        if board.winner[player.color]:
            player.gamePoints += 5
            match.gameWinner = True

        if match.isGameWinner():
            player.matchPoints += player.gamePoints
            player.gamePoints = 0
            player.jumps = 0
            if player.matchPoints > Match.MatchWin:
                match.matchWinner = True



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

    if board.defensePatterns[player.color] != []:
        print('Defense patterns: ')
        for defensePattern in board.defensePatterns[player.color]:
            print('  ' + defensePattern['name'] + positions(defensePattern['positions']))

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
