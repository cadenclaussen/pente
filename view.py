from tkinter import *
from view.images import *


currentPlayer = 0
beadsPlayed = 0


def main():
    root = Tk()
    root.title("Pente")
    root.geometry("760x760")

    window = LabelFrame(root, padx=1, pady=1, bg="grey")
    window.pack()

    header = LabelFrame(window, padx=10, pady=10)
    header.grid(row=0, column=0, columnspan=2, sticky=W+E)
    label = Label(header, text="Header Frame")
    label.pack()

    # Create the players pane
    players = LabelFrame(window, padx=10, pady=10, width=30)
    players.grid(row=1, column=0, sticky=N+S)
    label = Label(players, text="Players Frame")
    label.pack()

    # Create the players pane
    board = LabelFrame(window, padx=20, pady=20)
    board.grid(row=1, column=1)

    # Create the footer pane
    footer = LabelFrame(window, padx=20, pady=20)
    footer.grid(row=2, column=0, columnspan=2, sticky=W+E)
    label = Label(footer, text="Footer Frame")
    label.pack()

    # Add all the 19x19 images to the board pane to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for row in range(19):
        for column in range(19):
            image = getImage(row, column)
            label = Label(board, image=image, width=27, height=27, padx=0, pady=0)
            label.grid(row=row, column=column, padx=0, pady=0)
            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)
            label.bind("<Button-1>", playBead)

    root.mainloop()


def enter(e):
    global beadsPlayed

    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])

    print('Entering:', str(row) + '/' + str(column), 'beadsPlayed', beadsPlayed);
    if beadsPlayed == 0 and (row != 9 or column != 9):
        return

    if beadsPlayed == 2 and (row > 6 and row < 12 and column > 6 and column < 12):
        return

    # Show the players bead so they can visualize what it would look like
    e.widget.config(image=getBeadImage(row, column, currentPlayer))


def leave(e):
    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])
    print('Leaving:', str(row) + '/' + str(column));
    e.widget.config(image=getImage(row, column))


def playBead(e):
    global currentPlayer, beadsPlayed

    row = int(e.widget.grid_info()['row'])
    column = int(e.widget.grid_info()['column'])
    print('playing bead:', str(row) + '/' + str(column), 'beadsPlayed', beadsPlayed);

    if beadsPlayed == 0 and (row != 9 or column != 9):
        print('Opening move must be at 9,9');
        return

    if int(beadsPlayed) == 1 and (row > 6 and row < 12 and column > 6 and column < 12):
        print('Second move must be ...');
        return

    e.widget.config(image=getBeadImage(row, column, currentPlayer))
    e.widget.unbind("<Enter>")
    e.widget.unbind("<Leave>")
    e.widget.unbind("<Button-1>")
    nextPlayer()


def nextPlayer():
    global currentPlayer, beadsPlayed
    beadsPlayed += 1
    if currentPlayer == 0:
        currentPlayer = 1
    else:
        currentPlayer = 0


main()
