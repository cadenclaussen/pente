from tkinter import *
from tkinter import ttk
from images import *
import controller

boardFrame = None
rightMarginFrame = None
statusFrame = None

statusWidgets = []
weightLabels = []
moveLabels = []

match = None
highlights = []
hint = None
hintOption = False

Helv40 = ('Helvetica', 40)
Helv18 = ('Helvetica', 18)
Helv14 = ('Helvetica', 14)
Helv8 = ('Helvetica', 8)


# Here are what the primary UI Frames look like with
# height/width:
#
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
#
def main():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

    root = Tk()
    root.title('Pente')
    root.geometry('790x775+20+20')
    root.resizable(False, False)

    HeaderHeight = 1
    FooterHeight = 10
    BoardHeight = 19
    StatusHeight = 5

    leftMarginFrame = Frame(root)
    rightMarginFrame = Frame(root)
    headerFrame = Frame(root)
    boardFrame = Frame(root)
    statusFrame = Frame(root)

    leftMarginFrame.grid(row=0, column=0, rowspan=(HeaderHeight + BoardHeight + StatusHeight), columnspan=2, sticky=N)
    rightMarginFrame.grid(row=0, column=22, rowspan=(HeaderHeight + BoardHeight + StatusHeight), columnspan=2, sticky=N)
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

    button = ttk.Button(statusFrame, text='Turn Hints On')
    button.grid(row=3, column=5, sticky=EW)
    button.bind('<Button-1>', toggleHintOption)

    newMatch(None)

    root.mainloop()


def toggleHintOption(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption
    if hintOption:
        hintOption = False
        e.widget.config(text='Turn Hints On')
        label = Label(boardFrame, image=getOpenImage(hint['x'], hint['y']), borderwidth=0)
        label.grid(row=hint['y'], column=hint['x'], padx=0, pady=0)
        label.bind('<Enter>', enterBoardPosition)
        label.bind('<Leave>', leaveBoardPosition)
        label.bind('<Button-1>', addBead)
    else:
        hintOption = True
        e.widget.config(text='Turn Hints Off')
        label = Label(boardFrame, image=getHintImage(hint['x'], hint['y']), borderwidth=0)
        label.grid(row=hint['y'], column=hint['x'], padx=0, pady=0)
        label.bind('<Enter>', enterBoardPosition)
        label.bind('<Leave>', leaveBoardPosition)
        label.bind('<Button-1>', addBead)


def newMatch(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption
    match = controller.newMatch()
    newGame(e)


def newGame(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption
    match = controller.newGame()
    initializeBoard()
    highlights = []
    updateUx()
    if not match.game.gameOver() and match.game.currentColor == 'Red':
        addBeadAI(hint['x'], hint['y'])


def initializeBoard():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

    # Add all the 19x19 images to the boardFrame to initialize the board
    # - For each spot on the board, bind enterBoardPosition(), leaveBoardPosition(), and addBead() functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for y in range(19):
        for x in range(19):
            label = Label(boardFrame, image=getOpenImage(x, y), borderwidth=0)
            label.grid(row=y, column=x, padx=0, pady=0)
            label.bind('<Enter>', enterBoardPosition)
            label.bind('<Leave>', leaveBoardPosition)
            label.bind('<Button-1>', addBead)


# Invoked when the mouse enters one of the 19x19 grid position on the board
# As a result of the rollover, show the player's bead as they roll over
# each board position so they can visualize what it would look like if
# they played at that position on the board.
def enterBoardPosition(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

    if match.game.gameOver():
        return

    # Get the x and y board positions the mouse entered
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # If a bead is already played just update the right margin of the Ux
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

    # Note: This temporary bead removed by the leaveBoardPosition() function when
    # the player's mouse leaves the position.
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))
    updateRightMargin(x, y)



# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leaveBoardPosition() function.  Since the enter event
# previously invoked the enterBoardPosition() function temporarily putting a bead
# in the spot, the leaveBoardPosition() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leaveBoardPosition(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

    if match.game.gameOver():
        return

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # If the "open" position is the hint, restore the hint
    if hintOption and x == hint['x'] and y == hint['y']:
        e.widget.config(image=getHintImage(x, y))
    else:
        e.widget.config(image=getOpenImage(x, y))


# Performs the same function as addBead but is directly called to support
# the AI player adding a bead.
def addBeadAI(x, y):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption
    label = Label(boardFrame, image=getBeadImage(x, y, match.game.currentColor), borderwidth=0)
    label.grid(row=y, column=x, padx=0, pady=0)
    label.bind('<Enter>', enterBoardPosition)
    match = controller.addBead(x, y)
    updateUx()


# Called as a result of a mouse click on one of the board's grid positions
def addBead(e):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

    if match.game.gameOver():
        return

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
        label.bind('<Enter>', enterBoardPosition)
        label.bind('<Leave>', leaveBoardPosition)
        label.bind('<Button-1>', addBead)

    # Add the bead
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))
    e.widget.unbind('<Leave>')
    e.widget.unbind('<Button-1>')

    match = controller.addBead(x, y)
    updateUx()

    if not match.game.gameOver() and match.game.currentColor == 'Red':
        addBeadAI(hint['x'], hint['y'])


def updateUx():
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption

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
        label.bind('<Enter>', enterBoardPosition)
        label.bind('<Leave>', leaveBoardPosition)
        label.bind('<Button-1>', addBead)

    # Set the new highlights
    highlights = []
    for position in match.game.board.getAnnounces():
        highlights.append(position)
        x = position['x']
        y = position['y']
        label = Label(boardFrame, image=getHighlightedBeadImage(x, y, match.game.board.getBead(x, y)), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)

    # Add the hint
    hint = match.game.board.getHint()
    if hintOption:
        label = Label(boardFrame, image=getHintImage(hint['x'], hint['y']), borderwidth=0)
        label.grid(row=hint['y'], column=hint['x'], padx=0, pady=0)
        label.bind('<Enter>', enterBoardPosition)
        label.bind('<Leave>', leaveBoardPosition)
        label.bind('<Button-1>', addBead)

    # The following code displays:
    # - blue and red player jumps
    # - blue and red player game points
    # - blue and red player match points
    # - the button to start a new game or match if appropriate
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

    if match.game.gameOver() and match.matchOver():
        button = ttk.Button(statusFrame, text='New Match')
        button.grid(row=1, column=5, sticky='nw')
        button.bind('<Button-1>', newMatch)
        statusWidgets.append(button)
    elif match.game.gameOver():
        button = ttk.Button(statusFrame, text='New Game')
        button.grid(row=1, column=5, sticky=EW)
        button.bind('<Button-1>', newGame)
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


# The right margin frame displays information about each grid position
# a user can play on.  Specifically, what's the weight of the play, and
# what are all the offensive an defensive patterns that position
# contributes to.
def updateRightMargin(x, y):
    global boardFrame, rightMarginFrame, statusFrame, statusWidgets, highlights, match, hint, hintOption, weightLabels, moveLabels

    if not hintOption:
        return

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
