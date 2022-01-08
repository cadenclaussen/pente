from Player import Player
from Game import Game
from Board import Board


game = None
board = None
players = None
currentPlayer = None


def getGame():
    global game, board, players, currentPlayer
    return game


def getBoard():
    global game, board, players, currentPlayer
    return board


def getPlayers():
    global game, board, players, currentPlayer
    return players


def getCurrentPlayer():
    global game, board, players, currentPlayer
    return currentPlayer


def newGame():
    global game, board, players, currentPlayer

    game = Game()
    game.beadsPlayed = 0
    currentPlayer = 0


def playBead(position):
    global game, board, players, currentPlayer

    print("Controller: playing bead at " + str(position["row"]) + ", " + str(position["col"]));
    game.beadsPlayed += 1
    if currentPlayer == 0:
        currentPlayer = 1
    else:
        currentPlayer = 0
