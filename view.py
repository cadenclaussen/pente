# import tkinter module
import tkinter as tk
from tkinter import ttk
from lib.images import *
import controller


boardFrame = None
game = None
board = None
players = None
currentPlayer = None


def main():
    global board, game, players, currentPlayer

    # creating main tkinter window/toplevel
    root = tk.Tk()
    root.title("Pente v0.1")
    root.geometry("900x900+10+10")
    root.resizable(False, False)

    header = ttk.Frame(root)
    player1 = ttk.Frame(root)
    boardFrame = ttk.Frame(root)
    player2 = ttk.Frame(root)
    footer = ttk.Frame(root)

    header.grid(row=0, column=0, rowspan=2, columnspan=25)
    player1.grid(row=3, column=0, rowspan=19, columnspan=3)
    boardFrame.grid(row=3, column=3, rowspan=19, columnspan=19)
    player2.grid(row=3, column=22, rowspan=19, columnspan=3)
    footer.grid(row=22, column=0, rowspan=2, columnspan=25)

    ttk.Label(header, text='Pente v1.0').grid(row=0, column=0, sticky="ew")
    ttk.Label(header, text='by Caden Claussen and Shane Claussen').grid(row=1, column=0, sticky="nsew")

    newGame(boardFrame)
    updatePlayers(player1, player2, players)

    ttk.Label(footer, text='Footer 1').grid(row=0, column=0, sticky="nsew")
    ttk.Label(footer, text='Footer 2').grid(row=1, column=0, sticky="nsew")

    root.mainloop()


def updatePlayers(player1, player2, players):
    ttk.Label(player1, text="Name").grid(row=0, column=0, sticky="e")
    ttk.Label(player1, text=players[0].name).grid(row=0, column=1, sticky="w")

    ttk.Label(player1, text="Color").grid(row=1, column=0, sticky="e")
    ttk.Label(player1, text=players[0].color).grid(row=1, column=1, sticky="w")

    ttk.Label(player1, text="Jumps").grid(row=2, column=0, sticky="e")
    ttk.Label(player1, text=players[0].jumps).grid(row=2, column=1, sticky="w")

    ttk.Label(player1, text="Points").grid(row=3, column=0, sticky="e")
    ttk.Label(player1, text=players[0].score).grid(row=3, column=1, sticky="w")


    ttk.Label(player2, text="Name").grid(row=0, column=0, sticky="e")
    ttk.Label(player2, text=players[1].name).grid(row=0, column=1, sticky="w")

    ttk.Label(player2, text="Color").grid(row=1, column=0, sticky="e")
    ttk.Label(player2, text=players[1].color).grid(row=1, column=1, sticky="w")

    ttk.Label(player2, text="Jumps").grid(row=2, column=0, sticky="e")
    ttk.Label(player2, text=players[1].jumps).grid(row=2, column=1, sticky="w")

    ttk.Label(player2, text="Points").grid(row=3, column=0, sticky="e")
    ttk.Label(player2, text=players[1].score).grid(row=3, column=1, sticky="w")


def newGame(boardFrame):
    global board, game, players, currentPlayer

    # Add all the 19x19 images to the boardFrame to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for row in range(19):
        for column in range(19):
            label = ttk.Label(boardFrame, image=getImage(row, column), borderwidth=0)
            label.grid(row=row, column=column)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    game, board, players, currentPlayer = controller.newGame()


def enter(e):
    global game, board, players, currentPlayer

    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])

    if game.beadsPlayed == 0 and (row != 9 or column != 9):
        return

    if game.beadsPlayed == 2 and (row > 6 and row < 12 and column > 6 and column < 12):
        return

    # Show the players bead so they can visualize what it would look
    # like in that position on the board.  Note: This temporary bead
    # is removed by the leave() function when the player's mouse
    # leaves the position.
    e.widget.config(image=getBeadImage(row, column, currentPlayer.color))


# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leave() function.  Since the enter event
# previously invoked the enter() function temporarily putting a bead
# in the spot, the leave() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leave(e):
    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])
    e.widget.config(image=getImage(row, column))


def playBead(e):
    global game, board, players, currentPlayer

    # Get the row and column the bead was played at
    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])

    if game.beadsPlayed == 0 and (row != 9 or column != 9):
        return

    if game. beadsPlayed == 2 and (row > 6 and row < 12 and column > 6 and column < 12):
        return

    e.widget.config(image=getBeadImage(row, column, currentPlayer.color))
    e.widget.unbind("<Enter>")
    e.widget.unbind("<Leave>")
    e.widget.unbind("<Button-1>")


    game, board, players, currentPlayer, beadsToRemove = controller.playBead({ "row": row, "column": column })
    if beadsToRemove != []:
        for position in beadsToRemove:
            row = position["row"]
            column = position["column"]
            image = getImage(row, column)
            label = Label(boardLabelFrame, image=image, width=27, height=27, padx=0, pady=0)
            label.grid(row=row, column=column, padx=0, pady=0)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)
    board.beadsToRemove = []


    if (game.isWinner()):
        newGame()


main()
