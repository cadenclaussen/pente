from tkinter import *
from images import *
import controller


boardFrame = None
player1 = None
player2 = None
beadHighlights = []
moveHighlights = []
lastPlayedBead = None

match = None
board = None
players = None
currentPlayer = None


def main():
    global boardFrame, player1Frame, matchFrame, player2Frame, match, board, players, currentPlayer

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

    player1Frame = Frame(footerFrame, height=32)
    matchFrame = Frame(footerFrame, height=32)
    player2Frame = Frame(footerFrame, height=32)
    player1Frame.grid(row=0, column=0, rowspan=7, columnspan=5, padx=30, pady=5)
    matchFrame.grid(row=0, column=5, rowspan=7, columnspan=9, padx=30, pady=5)
    player2Frame.grid(row=0, column=14, rowspan=7, columnspan=5, padx=30, pady=5)

    Label(headerFrame, text='Pente v0.1', font=('Helvetica', 40)).grid(row=0, column=0, sticky='ew')
    Label(headerFrame, text='by Caden Claussen and Shane Claussen', font=('Helvetica', 8)).grid(row=1, column=0, sticky='nsew')

    newMatch()

    root.mainloop()


def newMatch():
    global match, board, players, currentPlayer
    match, board, players, currentPlayer = controller.newMatch()
    newGame()


def newGame():
    global match, board, players, currentPlayer, beadHighlights, moveHighlights
    initializeBoard()
    match, board, players, currentPlayer = controller.newGame()
    beadHighlights = []
    moveHighlights = []
    updateUx(match, board, players, currentPlayer)


def initializeBoard():
    global boardFrame

    # Add all the 19x19 images to the boardFrame to initialize the board
    # - For each spot on the board, bind enter, leave, and playBead functions
    # - Upper left is [0, 0], bottom right is [18, 18], middle is [9, 9]
    for y in range(19):
        for x in range(19):
            label = Label(boardFrame, image=getImage(x, y, False), borderwidth=0)
            label.grid(row=y, column=x, padx=0, pady=0)
            label.bind('<Enter>', enter)
            label.bind('<Leave>', leave)
            label.bind('<Button-1>', playBead)


def enter(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, match, board, players, currentPlayer

    # Get the x and y board positions the mouse entered
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # The very first move must be in the center
    if match.beadsPlayed == 0 and (x != 9 or y != 9):
        return

    # The starting player's second move must be 3 spaces away from the
    # center position
    if match.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    # Show the player's bead as they roll over each board position so
    # they can visualize what it would look like if they played at
    # that position on the board.
    #
    # Note: This temporary bead removed by the leave() function when
    # the player's mouse leaves the position.
    e.widget.config(image=getBeadImage(x, y, currentPlayer.color, False))


# When the mouse enters the board, if the spot is empty, the leave
# event will be bound to the leave() function.  Since the enter event
# previously invoked the enter() function temporarily putting a bead
# in the spot, the leave() function is responsible for setting the
# spot back to the image that indicates the spot is empty.
def leave(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, match, board, players, currentPlayer, moveHighlights

    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    for position in moveHighlights:
        if x == position['x'] and y == position['y']:
            e.widget.config(image=getImage(x, y, True))
            return

    e.widget.config(image=getImage(x, y, False))



def playBead(e):
    global boardFrame, player1Frame, matchFrame, player2Frame, match, board, players, currentPlayer, lastPlayedBead

    # Get the position the bead was played at
    x = int(e.widget.grid_info()['column'])
    y = int(e.widget.grid_info()['row'])

    # The very first move must be in the center, if not, ignore the mouse click
    if match.beadsPlayed == 0 and (y != 9 or x != 9):
        return

    # The starting player's second move must be 3 spaces away from the
    # center position so ignore the mouse click
    if match.beadsPlayed == 2 and (y > 6 and y < 12 and x > 6 and x < 12):
        return

    lastPlayedBead = { 'x': x, 'y': y }
    e.widget.config(image=getBeadImage(x, y, currentPlayer.color, False))
    e.widget.unbind('<Enter>')
    e.widget.unbind('<Leave>')
    e.widget.unbind('<Button-1>')

    match, board, players, currentPlayer = controller.playBead(x, y)
    updateUx(match, board, players, currentPlayer)


def updateUx(match, board, players, currentPlayer):
    global boardFrame, player1Frame, matchFrame, player2Frame, beadHighlights, moveHighlights, lastPlayedBead

    # Clear the old beadHighlights
    for position in beadHighlights:
        x = position['x']
        y = position['y']
        label = Label(boardFrame, image=getBeadImage(x, y, board.getBead(x, y), False), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)

    # Clear the old moveHighlights
    for position in moveHighlights:
        x = position['x']
        y = position['y']
        if x == lastPlayedBead['x'] and y == lastPlayedBead['y']:
            continue
        label = Label(boardFrame, image=getImage(x, y, False), borderwidth=0)
        label.grid(row=y, column=x, padx=0, pady=0)
        label.bind('<Enter>', enter)
        label.bind('<Leave>', leave)
        label.bind('<Button-1>', playBead)

    # Remove any jumped beads
    for jumpPattern in board.jumpPatterns:
        for position in jumpPattern['positions']:
            x = position['x']
            y = position['y']
            label = Label(boardFrame, image=getImage(x, y, False), borderwidth=0)
            label.grid(row=y, column=x, padx=0, pady=0)
            label.bind('<Enter>', enter)
            label.bind('<Leave>', leave)
            label.bind('<Button-1>', playBead)

    # Set the new beadHiglights
    beadHighlights = []
    for player in players:
        for announcePattern in board.announcePatterns[player.color]:
            for position in announcePattern['positions']:
                beadHighlights.append(position)
                x = position['x']
                y = position['y']
                label = Label(boardFrame, image=getBeadImage(x, y, board.getBead(x, y), True), borderwidth=0)
                label.grid(row=y, column=x, padx=0, pady=0)

    # Set the new moveHiglights
    moveHighlights = []
    for player in players:
        for movePattern in board.movePatterns[player.color]:
            for position in movePattern['positions']:
                moveHighlights.append(position)
                x = position['x']
                y = position['y']
                label = Label(boardFrame, image=getImage(x, y, True), borderwidth=0)
                label.grid(row=y, column=x, padx=0, pady=0)
                label.bind('<Enter>', enter)
                label.bind('<Leave>', leave)
                label.bind('<Button-1>', playBead)

    updateMatchDashboard()
    updatePlayerDashboard(player1Frame, players[0])
    updatePlayerDashboard(player2Frame, players[1])

    if match.matchWinner:
        newMatch()
    else:
        if match.gameWinner:
            newGame()


def updateMatchDashboard():
    global boardFrame, player1Frame, matchFrame, player2Frame, match, board, players, currentPlayer

    Label(matchFrame, text='Match').grid(row=0, column=3, stick='n')

    Label(matchFrame, text='Game: ' + str(match.gameCount)).grid(row=1, column=3, stick='ew')

    Label(matchFrame, image=getImageByColor(players[0].color, False)).grid(row=2, column=2, stick='ew')
    Label(matchFrame, text=players[0].matchPoints).grid(row=3, column=2, stick='ew')

    Label(matchFrame, image=getImageByColor(players[1].color, False)).grid(row=2, column=4, stick='ew')
    Label(matchFrame, text=players[1].matchPoints).grid(row=3, column=4, stick='ew')


def updatePlayerDashboard(frame, player):
    global boardFrame, matchFrame, match, board, players, currentPlayer

    Label(frame, text=player.name).grid(row=0, column=2, stick='ew')
    highlightCurrentPlayerBead = False
    if currentPlayer.name == player.name:
        highlightCurrentPlayerBead = True
    Label(frame, image=getImageByColor(player.color, highlightCurrentPlayerBead)).grid(row=1, column=2, stick='ew')

    Label(frame, text='Jumps: ' + str(player.jumps)).grid(row=2, column=2, sticky='e')
    Label(frame, text='Points: ' + str(player.gamePoints)).grid(row=3, column=2, sticky='e')


main()
