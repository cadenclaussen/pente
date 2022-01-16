# points
# highlight announces
import random
from Player import Player
from Game import Game
from Board import Board


game = None
board = None
players = None
currentPlayer = None


def newGame():
    global game, board, players, currentPlayer
    game = Game()
    players = [ Player("Shane", "Blue", 0), Player("Caden", "Green", 1) ]
    board = Board(players)
    currentPlayer = random.choice(players)

    __ux()
    return [ game, board, players, currentPlayer ]


def playBead(x, y):
    global game, board, players, currentPlayer

    currentPlayer.points = 0

    board.playBead(x, y, currentPlayer.color)
    game.beadsPlayed += 1

    if board.findJumpPatterns(x, y, currentPlayer.color):
        currentPlayer.jumps += len(board.jumpPatterns)
        if currentPlayer.jumps >= 5:
            game.winner = True
    currentPlayer.points += currentPlayer.jumps

    if board.findWinningPatterns(currentPlayer.color):
        currentPlayer.points += 5
        game.winner = True

    board.findAnnouncePatterns(currentPlayer.color)

    if board.findPointPatterns(currentPlayer.color):
        currentPlayer.points += len(board.pointPatterns[currentPlayer.color])

    __nextPlayer()

    board.findAnnouncePatterns(currentPlayer.color)

    currentPlayer.points = 0
    currentPlayer.points += currentPlayer.jumps
    if board.findPointPatterns(currentPlayer.color):
        currentPlayer.points += len(board.pointPatterns[currentPlayer.color])

    __ux()
    return game, board, players, currentPlayer


def __ux():
    global game, board, players, currentPlayer
    print(board)
    print()
    __printPlayer(players[0])
    __printPlayer(players[1])
    print()
    print("Winner: " + str(game.winner))
    print()
    print("Next Move: " + currentPlayer.name)


def __printPlayer(player):
    print(player.name)
    print("------------------------------")
    print("Jumps: " + str(player.jumps))
    print("Points: " + str(player.points))

    if board.pointPatterns[player.color] != []:
        print("Point patterns: ")
        for pointPattern in board.pointPatterns[player.color]:
            print(pointPattern["name"] + __positions(pointPattern["positions"]))

    if board.announcePatterns[player.color] != []:
        print("Announce patterns: ")
        for announcePattern in board.announcePatterns[player.color]:
            print(announcePattern["name"] + __positions(announcePattern["positions"]))

    print()


def __positions(positions):
    s = ""
    for position in positions:
        s += " (" + str(position["x"]) + "," + str(position["y"]) + ")"
    return s


def __nextPlayer():
    global game, board, players, currentPlayer
    if currentPlayer.key == 0:
        currentPlayer = players[1]
    else:
        currentPlayer = players[0]
