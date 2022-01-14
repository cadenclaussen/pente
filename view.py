from tkinter import *
from lib.images import *
import controller


game = None
board = None
players = None
currentPlayer = None
boardLabelFrame = None


def main():
    global boardLabelFrame, game, board, players, currentPlayer

    root = Tk()
    root.title("Pente")
    root.geometry("760x760")

    windowFrame = LabelFrame(root, padx=1, pady=1, bg="grey")
    windowFrame.pack()

    headerLabelFrame = LabelFrame(windowFrame, padx=10, pady=10)
    headerLabelFrame.grid(row=0, column=0, columnspan=2, sticky=W+E)
    label = Label(headerLabelFrame, text="Header Frame")
    label.pack()

    # Create the players pane
    playersLabelFrame = LabelFrame(windowFrame, padx=10, pady=10, width=30)
    playersLabelFrame.grid(row=1, column=0, sticky=N+S)
    label = Label(playersLabelFrame, text="Players Frame")
    label.pack()

    # Create the players pane
    boardLabelFrame = LabelFrame(windowFrame, padx=20, pady=20)
    boardLabelFrame.grid(row=1, column=1)

    # Create the footer pane
    footer = LabelFrame(windowFrame, padx=20, pady=20)
    footer.grid(row=2, column=0, columnspan=2, sticky=W+E)
    label = Label(footer, text="Footer Frame")
    label.pack()

    # Add all the 19x19 images to the board pane to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for row in range(19):
        for column in range(19):
            image = getImage(row, column)
            label = Label(boardLabelFrame, image=image, width=27, height=27, padx=0, pady=0)
            label.grid(row=row, column=column, padx=0, pady=0)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    newGame()


    root.mainloop()


def newGame():
    global boardLabelFrame, game, board, players, currentPlayer

    # Add all the 19x19 images to the board pane to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for row in range(19):
        for column in range(19):
            image = getImage(row, column)
            label = Label(boardLabelFrame, image=image, width=27, height=27, padx=0, pady=0)
            label.grid(row=row, column=column, padx=0, pady=0)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    # Controller logic
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
