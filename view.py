# import tkinter module
import tkinter as tk
# from tkinter import ttk
from lib.images import *
import controller


boardFrame = None
player1 = None
player2 = None
highlights = []

game = None
board = None
players = None
currentPlayer = None


def main():
    global boardFrame, player1Frame, matchFrame, player2Frame, game, board, players, currentPlayer

    # creating main tkinter window/toplevel
    root = tk.Tk()
    root.title("Pente")
    root.geometry("590x775+20+20")
    root.resizable(False, False)

    headerFrame = tk.Frame(root)
    boardFrame = tk.Frame(root)
    footerFrame = tk.Frame(root)
    headerFrame.grid(row=0, column=0, rowspan=5, columnspan=19)
    boardFrame.grid(row=5, column=0, rowspan=19, columnspan=19)
    footerFrame.grid(row=24, column=0, rowspan=7, columnspan=19)

    player1Frame = tk.Frame(footerFrame, height=32)
    matchFrame = tk.Frame(footerFrame, height=32)
    player2Frame = tk.Frame(footerFrame, height=32)
    player1Frame.grid(row=0, column=0, rowspan=7, columnspan=5, padx=30, pady=5)
    matchFrame.grid(row=0, column=5, rowspan=7, columnspan=9, padx=30, pady=5)
    player2Frame.grid(row=0, column=14, rowspan=7, columnspan=5, padx=30, pady=5)

    tk.Label(headerFrame, text='Pente v0.1', font=("Helvetica", 40)).grid(row=0, column=0, sticky="ew")
    tk.Label(headerFrame, text='by Caden Claussen and Shane Claussen', font=("Helvetica", 8)).grid(row=1, column=0, sticky="nsew")

    newGame(boardFrame)

    root.mainloop()


def newGame(boardFrame):
    global game, board, players, currentPlayer

    # Add all the 19x19 images to the boardFrame to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for y in range(19):
        for x in range(19):
            label = tk.Label(boardFrame, image=getImage(x, y, False), borderwidth=0)
            label.grid(row=y, column=x)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    game, board, players, currentPlayer = controller.newGame()
    updateUx(game, board, players, currentPlayer)


def enter(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, game, board, players, currentPlayer

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    if game.beadsPlayed == 0 and (x != 9 or y != 9):
        return

    if game.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    # Show the players bead so they can visualize what it would look
    # like in that position on the board.  Note: This temporary bead
    # is removed by the leave() function when the player's mouse
    # leaves the position.
    e.widget.config(image=getBeadImage(x, y, currentPlayer.color, False))


# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leave() function.  Since the enter event
# previously invoked the enter() function temporarily putting a bead
# in the spot, the leave() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leave(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, game, board, players, currentPlayer

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])
    e.widget.config(image=getImage(x, y, False))


def playBead(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, game, board, players, currentPlayer

    # Get the row and column the bead was played at
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    if game.beadsPlayed == 0 and (y != 9 or x != 9):
        return

    if game.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    e.widget.config(image=getBeadImage(x, y, currentPlayer.color, False))
    e.widget.unbind("<Enter>")
    e.widget.unbind("<Leave>")
    e.widget.unbind("<Button-1>")

    game, board, players, currentPlayer = controller.playBead(x, y)
    updateUx(game, board, players, currentPlayer)


def updateUx(game, board, players, currentPlayer):
    global boardFrame, player1Frame, matchFrame, player2Frame, highlights

    # Clear the old highlights
    for position in highlights:
        x = position["x"]
        y = position["y"]
        label = tk.Label(boardFrame, image=getBeadImage(x, y, board.getBead(x, y), False), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)

    # Remove any jumped beads
    for jumpPattern in board.jumpPatterns:
        for position in jumpPattern["positions"]:
            x = position["x"]
            y = position["y"]
            label = tk.Label(boardFrame, image=getImage(x, y, False), borderwidth=0)
            label.grid(row=y, column=x, padx=0, pady=0)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    # Set the new higlights
    highlights = []
    for player in players:
        for announcePattern in board.announcePatterns[player.color]:
            for position in announcePattern['positions']:
                highlights.append(position)
                print(player.color + ': ' + str(position))
                x = position['x']
                y = position['y']
                label = tk.Label(boardFrame, image=getBeadImage(x, y, player.color, True), borderwidth=0)
                label.grid(row=y, column=x, padx=0, pady=0)

    __uxMatch(matchFrame, players)
    __uxPlayer(player1Frame, players[0])
    __uxPlayer(player2Frame, players[1])

    if (game.isWinner()):
        newGame(boardFrame)


def __uxMatch(frame, players):
    tk.Label(frame, text="Match").grid(row=0, column=3, stick="n")

    tk.Label(frame, image=getImageByColor(players[0].color, False)).grid(row=1, column=2, stick="ew")
    tk.Label(frame, text="19").grid(row=2, column=2, stick="ew")

    tk.Label(frame, image=getImageByColor(players[1].color, False)).grid(row=1, column=4, stick="ew")
    tk.Label(frame, text="19").grid(row=2, column=4, stick="ew")


def __uxPlayer(frame, player):
    tk.Label(frame, text=player.name).grid(row=0, column=2, stick="ew")
    tk.Label(frame, image=getImageByColor(player.color, False)).grid(row=1, column=2, stick="ew")

    tk.Label(frame, text="Jumps").grid(row=2, column=1, sticky="e")
    tk.Label(frame, text=player.jumps).grid(row=2, column=3, sticky="w")

    tk.Label(frame, text="Points").grid(row=3, column=1, sticky="e")
    tk.Label(frame, text=player.points).grid(row=3, column=3, sticky="w")


main()
