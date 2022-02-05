from tkinter import *
from tkinter import ttk
from images import *
import controller


boardFrame = None
rightMarginFrame = None
statusFrame = None
hint = None

statusWidgets = []
hintLabel = None
weightLabels = []
moveLabels = []

highlights = []
match = None

Helv40 = ('Helvetica', 40)
Helv18 = ('Helvetica', 18)
Helv14 = ('Helvetica', 14)
Helv8 = ('Helvetica', 8)


def main():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    root = Tk()
    root.title('Pente')
    root.geometry('790x775+20+20')
    root.resizable(False, False)

    HeaderHeight = 1
    FooterHeight = 10
    BoardHeight = 19
    StatusHeight = 5
    ActionHeight = 2

    #    +-- 2 --+------ 19 ------+-- 2 --+
    #    |       |                |       |
    #    |       2     Header     2       |
    #    |       |                |       |
    #    |       +----------------+       |
    #    |       |                |       |
    #    |       |                |       |
    #    |  LM   19    Board     19  RM   |
    #    |       |                |       |
    #    |       |                |       |
    #    |       +----------------+       |
    #    |       |                |       |
    #    |       5     Status     5       |
    #    |       |                |       |
    #    +-- 2 --+------ 19 ------+-- 2 --+

    leftMarginFrame = Frame(root)
    rightMarginFrame = Frame(root)
    headerFrame = Frame(root)
    boardFrame = Frame(root)
    statusFrame = Frame(root)

    leftMarginFrame.grid(row=0, column=0, rowspan=(HeaderHeight + BoardHeight + StatusHeight + ActionHeight), columnspan=2, sticky=N)
    rightMarginFrame.grid(row=0, column=22, rowspan=(HeaderHeight + BoardHeight + StatusHeight + ActionHeight), columnspan=2, sticky=N)
    headerFrame.grid(row=0, column=3, rowspan=2, columnspan=19)
    boardFrame.grid(row=2, column=3, rowspan=19, columnspan=19)
    statusFrame.grid(row=21, column=3, rowspan=5, columnspan=19)
    for row in range(20):
        leftMarginFrame.grid_rowconfigure(row, minsize=30, weight=1)
        rightMarginFrame.grid_rowconfigure(row, minsize=30, weight=1)
    leftMarginFrame.grid_columnconfigure(0, minsize=30, weight=1)
    for column in range(9):
        statusFrame.grid_columnconfigure(column, minsize=30, weight=1)

    Label(headerFrame, text='Pente v0.2', font=Helv40).grid(row=0, column=0, sticky=EW)
    Label(headerFrame, text='by Shane Claussen and Caden Claussen', font=Helv8).grid(row=1, column=0, sticky=EW)

    newMatch(None)

    root.mainloop()


def newMatch(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint
    match = controller.newMatch()
    newGame(e)


def newGame(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint
    match = controller.newGame()
    initializeBoard()
    highlights = []
    updateUx()


def initializeBoard():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    # Add all the 19x19 images to the boardFrame to initialize the board
    # - For each spot on the board, bind enter(), leave(), and addBead() functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for y in range(19):
        for x in range(19):
            label = Label(boardFrame, image=getOpenImage(x, y), borderwidth=0)
            label.grid(row=y, column=x, padx=0, pady=0)
            label.bind('<Enter>', enter)
            label.bind('<Leave>', leave)
            label.bind('<Button-1>', addBead)


def enter(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    # Get the x and y board positions the mouse entered
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    if match.game.board.getBead(x, y) != 'Open':
        updateRightMargin(x, y)
        return

    # The very first move must be in the center
    if match.game.beadsPlayed == 0 and (x != 9 or y != 9):
        updateRightMargin(x, y)
        return

    # The starting color's second move must be 3 spaces away from the
    # center position
    if match.game.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        updateRightMargin(x, y)
        return

    # Show the player's bead as they roll over each board position so
    # they can visualize what it would look like if they played at
    # that position on the board.
    #
    # Note: This temporary bead removed by the leave() function when
    # the player's mouse leaves the position.
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))
    updateRightMargin(x, y)



# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leave() function.  Since the enter event
# previously invoked the enter() function temporarily putting a bead
# in the spot, the leave() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leave(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    if x == hint['x'] and y == hint['y']:
        e.widget.config(image=getOpenImageOffense(x, y))
    else:
        e.widget.config(image=getOpenImage(x, y))


def addBead(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    # Get the position the bead was played at
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # The very first move must be in the center, if not, ignore the mouse click
    if match.game.beadsPlayed == 0 and (y != 9 or x != 9):
        return

    # The starting color's second move must be 3 spaces away from the
    # center position so ignore the mouse click
    if match.game.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    # Remove hint
    if x != hint['x'] or y != hint['y']:
        label = Label(boardFrame, image=getOpenImage(hint['x'], hint['y']), borderwidth=0)
        label.grid(row=hint['y'], column=hint['x'], padx=0, pady=0)
        label.bind('<Enter>', enter)
        label.bind('<Leave>', leave)
        label.bind('<Button-1>', addBead)

    # Add the bead
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))
    e.widget.unbind('<Leave>')
    e.widget.unbind('<Button-1>')

    match = controller.addBead(x, y)
    updateUx()


def updateUx():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint

    # Clear the old highlights revering back to the bead image without the highlight
    for position in highlights:
        x = position['x']
        y = position['y']
        label = Label(boardFrame, image=getBeadImage(x, y, match.game.board.getBead(x, y)), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)

    # Remove any jumped beads
    for position in match.game.board.getOpponentJumps():
        x = position['x']
        y = position['y']
        label = Label(boardFrame, image=getOpenImage(x, y), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)
        label.bind('<Enter>', enter)
        label.bind('<Leave>', leave)
        label.bind('<Button-1>', addBead)

    # Set the new highlights
    highlights = []
    for position in match.game.board.getHighlights():
        highlights.append(position)
        x = position['x']
        y = position['y']
        label = Label(boardFrame, image=getHighlightedBeadImage(x, y, match.game.board.getBead(x, y)), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)

    hint = match.game.board.getHint()
    label = Label(boardFrame, image=getOpenImageOffense(hint['x'], hint['y']), borderwidth=0)
    label.grid(row=hint['y'], column=hint['x'], padx=0, pady=0)
    label.bind('<Enter>', enter)
    label.bind('<Leave>', leave)
    label.bind('<Button-1>', addBead)

    for statusWidget in statusWidgets:
        statusWidget.destroy()

    Color1ColumnOffset = 0
    label = Label(statusFrame, image=getBead(match.colors[0], True if match.game.currentColor == match.colors[0] else False))
    label.grid(row=0, column=(Color1ColumnOffset + 1), stick='w')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Jumps', font=Helv14)
    label.grid(row=1, column=(Color1ColumnOffset + 0), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.game.jumps[match.colors[0]]))
    label.grid(row=1, column=(Color1ColumnOffset + 2), sticky='w')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Game Points', font=Helv14)
    label.grid(row=2, column=(Color1ColumnOffset + 0), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.game.points[match.colors[0]]))
    label.grid(row=2, column=(Color1ColumnOffset + 2), sticky='w')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Match Points', font=Helv14)
    label.grid(row=3, column=(Color1ColumnOffset + 0), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.points[match.colors[0]]))
    label.grid(row=3, column=(Color1ColumnOffset + 2), sticky='w')
    statusWidgets.append(label)

    if match.game.isWinner() and match.isWinner():
        button = ttk.Button(statusFrame, text='New Match')
        button .grid(row=1, column=5, sticky='nw')
        button .bind('<Button-1>', newMatch)
        statusWidgets.append(button)
    elif match.game.isWinner():
        print('Game winner')
        button = ttk.Button(statusFrame, text='New Game')
        button .grid(row=1, column=5, sticky=EW)
        button .bind('<Button-1>', newGame)
        statusWidgets.append(button)

    Color2ColumnOffset = 5
    label = Label(statusFrame, image=getBead(match.colors[1], True if match.game.currentColor == match.colors[1] else False))
    label.grid(row=0, column=(Color2ColumnOffset + 4), stick='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.game.jumps[match.colors[1]]))
    label.grid(row=1, column=(Color2ColumnOffset + 3), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Jumps', font=Helv14)
    label.grid(row=1, column=(Color2ColumnOffset + 5), sticky='w')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.game.points[match.colors[1]]))
    label.grid(row=2, column=(Color2ColumnOffset + 3), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Game Points', font=Helv14)
    label.grid(row=2, column=(Color2ColumnOffset + 5), sticky='w')
    statusWidgets.append(label)

    label = Label(statusFrame, text=str(match.points[match.colors[1]]))
    label.grid(row=3, column=(Color2ColumnOffset + 3), sticky='e')
    statusWidgets.append(label)

    label = Label(statusFrame, text='Match Points', font=Helv14)
    label.grid(row=3, column=(Color2ColumnOffset + 5), sticky='w')
    statusWidgets.append(label)


def updateRightMargin(x, y):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintLabel, weightLabels, moveLabels

    # Clear out the old weight and move labels
    for weightLabel in weightLabels:
        weightLabel.destroy()
    for moveLabel in moveLabels:
        moveLabel.destroy()

    HintRow = 3
    rowOffset = 0
    for move in match.game.board.getMoves(x, y):

        if rowOffset == 0:
            weight = match.game.board.getWeight(x, y)
            label = Label(rightMarginFrame, text='Hint', font=Helv18)
            label.grid(row=HintRow, column=0, sticky='nw')
            weightLabels.append(label)

            label = Label(rightMarginFrame, text='Position', font=Helv14)
            label.grid(row=HintRow + 1, column=0, sticky='nw')
            weightLabels.append(label)

            position = '({0:>2}, {1:>2})'.format(x, y)
            label = Label(rightMarginFrame, text=position, font=Helv14)
            label.grid(row=HintRow + 1, column=1, sticky='nw')
            weightLabels.append(label)

            label = Label(rightMarginFrame, text='Aggregate Weight', font=Helv14)
            label.grid(row=HintRow + 2, column=0, sticky='nw')
            weightLabels.append(label)

            label = Label(rightMarginFrame, text=str(weight), font=Helv14)
            label.grid(row=HintRow + 2, column=1, sticky='nw')
            weightLabels.append(label)

            label = Label(rightMarginFrame, text='Patterns', font=Helv18)
            label.grid(row=HintRow + 4 + rowOffset, column=0, sticky='nw')
            weightLabels.append(label)

        label = Label(rightMarginFrame, text=move['name'], font=Helv14)
        label.grid(row=(HintRow + 5 + rowOffset), column=0, sticky='nw')
        moveLabels.append(label)

        weight = str(move['weight'])
        label = Label(rightMarginFrame, text=weight, font=Helv14)
        label.grid(row=(HintRow + 5 + rowOffset), column=1, sticky='nw')
        moveLabels.append(label)

        rowOffset += 1


main()
