from tkinter import *
from images import *
import controller


boardFrame = None
color1Frame = None
color2Frame = None
matchFrame = None
lastMove = None

highlights = []
match = None


def main():
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

    root = Tk()
    root.title('Pente')
    root.geometry('590x775+20+20')
    root.resizable(False, False)

    headerFrame = Frame(root)
    boardFrame = Frame(root)
    footerFrame = Frame(root)
    headerFrame.grid(row=0, column=0, rowspan=5, columnspan=19)
    boardFrame.grid(row=5, column=0, rowspan=19, columnspan=19)
    footerFrame.grid(row=24, column=0, rowspan=7, columnspan=19)

    color1Frame = Frame(footerFrame, height=32)
    matchFrame = Frame(footerFrame, height=32)
    color2Frame = Frame(footerFrame, height=32)
    color1Frame.grid(row=0, column=0, rowspan=7, columnspan=5, padx=30, pady=5)
    matchFrame.grid(row=0, column=5, rowspan=7, columnspan=9, padx=30, pady=5)
    color2Frame.grid(row=0, column=14, rowspan=7, columnspan=5, padx=30, pady=5)

    Label(headerFrame, text='Pente v0.2', font=('Helvetica', 40)).grid(row=0, column=0, sticky='ew')
    Label(headerFrame, text='by Caden Claussen and Shane Claussen', font=('Helvetica', 8)).grid(row=1, column=0, sticky='nsew')

    newMatch()

    root.mainloop()


def newMatch():
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match
    match = controller.newMatch()
    newGame()


def newGame():
    print('Entering pente::newGame')
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match
    match = controller.newGame()
    print('pente::newGame() after call to controller.newGame()')
    print(match)
    initializeBoard()
    highlights = []
    updateUx()
    print('Exiting pente::newGame')


def initializeBoard():
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

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
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

    # Get the x and y board positions the mouse entered
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # The very first move must be in the center
    if match.game.beadsPlayed == 0 and (x != 9 or y != 9):
        return

    # The starting color's second move must be 3 spaces away from the
    # center position
    if match.game.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    # Show the player's bead as they roll over each board position so
    # they can visualize what it would look like if they played at
    # that position on the board.
    #
    # Note: This temporary bead removed by the leave() function when
    # the player's mouse leaves the position.
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))


# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leave() function.  Since the enter event
# previously invoked the enter() function temporarily putting a bead
# in the spot, the leave() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leave(e):
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # for position in defenseHighlights:
    #     if x == position['x'] and y == position['y']:
    #         e.widget.config(image=getOpenImageDefense(x, y))
    #         return

    # for position in offenseHighlights:
    #     if x == position['x'] and y == position['y']:
    #         e.widget.config(image=getOpenImageOffense(x, y))
    #         return

    e.widget.config(image=getOpenImage(x, y))



def addBead(e):
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

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

    lastMove = { 'x': x, 'y': y }
    e.widget.config(image=getBeadImage(x, y, match.game.currentColor))
    e.widget.unbind('<Enter>')
    e.widget.unbind('<Leave>')
    e.widget.unbind('<Button-1>')

    match = controller.addBead(x, y)
    updateUx()

    # TODO: Upate this logic to first display button(s)
    if match.isWinner():
        newMatch()
    else:
        if match.game.isWinner():
            newGame()


def updateUx():
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

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

    updateMatchDashboard()
    updateColorDashboard(color1Frame, match.colors[0])
    updateColorDashboard(color2Frame, match.colors[1])


def updateMatchDashboard():
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

    Label(matchFrame, text='Match').grid(row=0, column=3, stick='n')

    Label(matchFrame, text='Game: ' + str(match.gameCount)).grid(row=1, column=3, stick='ew')

    Label(matchFrame, image=getBead(match.colors[0], False)).grid(row=2, column=2, stick='ew')
    Label(matchFrame, text=match.points[match.colors[0]]).grid(row=3, column=2, stick='ew')

    Label(matchFrame, image=getBead(match.colors[1], False)).grid(row=2, column=4, stick='ew')
    Label(matchFrame, text=match.points[match.colors[1]]).grid(row=3, column=4, stick='ew')


def updateColorDashboard(frame, color):
    global boardFrame, color1Frame, color2Frame, matchFrame, highlights, lastMove, match

    highlightCurrentColorBead = False
    if match.game.currentColor == color:
        highlightCurrentColorBead = True
    Label(frame, image=getBead(color, highlightCurrentColorBead)).grid(row=1, column=2, stick='ew')

    Label(frame, text='Jumps: ' + str(match.game.jumps[color])).grid(row=2, column=2, sticky='e')
    Label(frame, text='Points: ' + str(match.game.points[color])).grid(row=3, column=2, sticky='e')


main()
