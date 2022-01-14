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


    # Create the whole root window that the game will be in
    # - set the title of the window
    # - set the size of the window
    root = Tk()
    root.title("Pente")
    root.geometry("900x900")


    # Create a LabelFrame as a child of the root window.
    # This will be the main frame for everything in the user interface.
    window = LabelFrame(root, padx=1, pady=1, bg="grey").pack()



    # Create a LabelFrame named header that will span the entire top of the user experience
    # - On row 1, spans all 3 columns
    header = LabelFrame(window, padx=10, pady=10, text="header").grid(row=0, column=0, rowspan=2, columnspan=3, sticky=W+E)
    # header1 = LabelFrame(header, padx=10, pady=10).grid(row=0, column=0)
    # header2 = LabelFrame(header, padx=10, pady=10).grid(row=1, column=0)
    label = Label(header, text="Pente v0.1").pack()
    label = Label(header, text="by Caden Claussen and Shane Claussen").pack()



    # # Create a LabelFrame named left on the left hand side of the playing board
    # # - On row 2, column 1
    # left = LabelFrame(window, padx=10, pady=10, width=30).grid(row=1, column=0, sticky=N+S)
    # label = Label(left, text="Left Frame").pack()



    # # Create a LabelFrame named board between the left and right label frames
    # # - On row 2, column 2
    # boardLabelFrame = LabelFrame(window, padx=20, pady=20)
    # boardLabelFrame.grid(row=2, column=1)

    # # Create a LabelFrame named right on the right hand side of the playing board on the 2nd row of the main window
    # # - On row 2, column 3
    # right = LabelFrame(window, padx=10, pady=10, width=30)
    # right.grid(row=2, column=2, sticky=N+S)
    # label = Label(right, text="Right Frame")
    # label.pack()


    # # Create a LabelFrame named footer below the board
    # # - On row 3, spans all 3 columns
    # footer = LabelFrame(window, padx=20, pady=20)
    # footer.grid(row=3, column=0, columnspan=3, sticky=W+E)
    # label = Label(footer, text="Footer Frame")
    # label.pack()


    # # Add all the 19x19 images to the board pane to initialize the board
    # # - For each spot on the board, bind enter, leave, and playBead functions
    # # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    # for row in range(19):
    #     for column in range(19):
    #         image = getImage(row, column)
    #         label = Label(boardLabelFrame, image=image, width=27, height=27, padx=0, pady=0)
    #         label.grid(row=row, column=column, padx=0, pady=0)
    #         label.bind("<Enter>", enter)
    #         label.bind("<Leave>", leave)
    #         label.bind("<Button-1>", playBead)

    # newGame()


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
