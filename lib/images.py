from PIL import Image as PI
from PIL import ImageTk


images = {}


# Returns a dictionary of images (key/value pair)
def getImages():
    global images

    # Singleton lazy load all the images
    if images == {}:
        images = __loadImages()

    return images


# Returns the image that goes at the row and colum in Pente
def getImage(row, column):
    global images

    # Singleton lazy load all the images
    if images == {}:
        images = __loadImages()

    return images[__getKey(row, column)]


# Returns the image that goes at the row and colum in Pente
# with a bead played in that location
def getBeadImage(row, column, currentPlayerColor):
    global images

    # Singleton lazy load all the images
    if images == {}:
        images = __loadImages()

    # currentPlayer should be either "Red" or "Blue"
    return images[__getKey(row, column) + currentPlayerColor]


def __getKey(row, column):
    global images

    # Center
    if row == 9 and column == 9:
        return 'center'

    # Handle the corners (outer corners)
    if row == 0 and column == 0:
        return 'cornerNorthwest'
    if row == 0 and column == 18:
        return 'cornerNortheast'
    if row == 18 and column == 0:
        return 'cornerSouthwest'
    if row == 18 and column == 18:
        return 'cornerSoutheast'

    # Bold T's (outer edge)
    if row == 0 and column == 9:
        return 'tNorthBold'
    if row == 9 and column == 0:
        return 'tWestBold'
    if row == 9 and column == 18:
        return 'tEastBold'
    if row == 18 and column == 9:
        return 'tSouthBold'

    # T's (outer edge)
    if row == 0:
        return 'tNorth'
    if column == 0:
        return 'tWest'
    if column == 18:
        return 'tEast'
    if row == 18:
        return 'tSouth'

    # Diamonds
    if (row == 6 and column == 6) or (row == 6 and column == 12) or (row == 12 and column == 6) or (row == 12 and column == 12):
        return 'diamond'
    if (row == 3 and column == 3) or (row == 3 and column == 15) or (row == 15 and column == 3) or (row == 15 and column == 15):
        return 'diamond'
    if (row == 3 and column == 9) or (row == 15 and column == 9):
        return 'diamondVertical'
    if (row == 9 and column == 3) or (row == 9 and column == 15):
        return 'diamondHorizontal'

    # Bold midway vertical and horizontal lines
    if column == 9:
        return 'vertical'
    if row == 9:
        return 'horizontal'

    # Default plus
    return 'plus'


def __loadImages():
    images = {}

    images['center'] = __load('lib/images/center.gif')
    images['centerBlue'] = __load('lib/images/centerBlue.gif')
    images['centerRed'] = __load('lib/images/centerRed.gif')

    images['diamond'] = __load('lib/images/diamond.gif')
    images['diamondBlue'] = __load('lib/images/plusblue.gif')
    images['diamondRed'] = __load('lib/images/plusred.gif')

    images['diamondVertical'] = __load('lib/images/diamondvertical.gif')
    images['diamondVerticalBlue'] = __load('lib/images/verticalblue.gif')
    images['diamondVerticalRed'] = __load('lib/images/verticalred.gif')

    images['diamondHorizontal'] = __loadTransposed('lib/images/diamondvertical.gif', PI.ROTATE_90)
    images['diamondHorizontalBlue'] = __loadTransposed('lib/images/verticalblue.gif', PI.ROTATE_90)
    images['diamondHorizontalRed'] = __loadTransposed('lib/images/verticalred.gif', PI.ROTATE_90)

    images['plus'] = __load('lib/images/plus.gif')
    images['plusBlue'] = __load('lib/images/plusblue.gif')
    images['plusRed'] = __load('lib/images/plusred.gif')

    images['vertical'] = __load('lib/images/vertical.gif')
    images['verticalBlue'] = __load('lib/images/verticalblue.gif')
    images['verticalRed'] = __load('lib/images/verticalred.gif')

    images['horizontal'] = __loadTransposed('lib/images/vertical.gif', PI.ROTATE_90)
    images['horizontalBlue'] = __loadTransposed('lib/images/verticalblue.gif', PI.ROTATE_90)
    images['horizontalRed'] = __loadTransposed('lib/images/verticalred.gif', PI.ROTATE_90)

    images['tNorth'] = __load('lib/images/t.gif')
    images['tNorthBlue'] = __load('lib/images/tblue.gif')
    images['tNorthRed'] = __load('lib/images/tred.gif')

    images['tSouth'] = __loadTransposed('lib/images/t.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBlue'] = __loadTransposed('lib/images/tblue.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthRed'] = __loadTransposed('lib/images/tred.gif', PI.FLIP_TOP_BOTTOM)

    images['tEast'] = __loadTransposed('lib/images/t.gif', PI.ROTATE_270)
    images['tEastBlue'] = __loadTransposed('lib/images/tblue.gif', PI.ROTATE_270)
    images['tEastRed'] = __loadTransposed('lib/images/tred.gif', PI.ROTATE_270)

    images['tWest'] = __loadTransposed('lib/images/t.gif', PI.ROTATE_90)
    images['tWestBlue'] = __loadTransposed('lib/images/tblue.gif', PI.ROTATE_90)
    images['tWestRed'] = __loadTransposed('lib/images/tred.gif', PI.ROTATE_90)

    images['tNorthBold'] = __load('lib/images/tbold.gif')
    images['tNorthBoldBlue'] = __load('lib/images/tboldblue.gif')
    images['tNorthBoldRed'] = __load('lib/images/tboldred.gif')

    images['tSouthBold'] = __loadTransposed('lib/images/tbold.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBoldBlue'] = __loadTransposed('lib/images/tboldblue.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBoldRed'] = __loadTransposed('lib/images/tboldred.gif', PI.FLIP_TOP_BOTTOM)

    images['tEastBold'] = __loadTransposed('lib/images/tbold.gif', PI.ROTATE_270)
    images['tEastBoldBlue'] = __loadTransposed('lib/images/tboldblue.gif', PI.ROTATE_270)
    images['tEastBoldRed'] = __loadTransposed('lib/images/tboldred.gif', PI.ROTATE_270)

    images['tWestBold'] = __loadTransposed('lib/images/tbold.gif', PI.ROTATE_90)
    images['tWestBoldBlue'] = __loadTransposed('lib/images/tboldblue.gif', PI.ROTATE_90)
    images['tWestBoldRed'] = __loadTransposed('lib/images/tboldred.gif', PI.ROTATE_90)

    images['cornerNorthwest'] = __load('lib/images/corner.gif')
    images['cornerNorthwestBlue'] = __load('lib/images/cornerBlue.gif')
    images['cornerNorthwestRed'] = __load('lib/images/cornerRed.gif')

    images['cornerNortheast'] = __loadTransposed('lib/images/corner.gif', PI.FLIP_LEFT_RIGHT)
    images['cornerNortheastBlue'] = __loadTransposed('lib/images/cornerBlue.gif', PI.FLIP_LEFT_RIGHT)
    images['cornerNortheastRed'] = __loadTransposed('lib/images/cornerRed.gif', PI.FLIP_LEFT_RIGHT)

    images['cornerSouthwest'] = __loadTransposed('lib/images/corner.gif', PI.FLIP_TOP_BOTTOM)
    images['cornerSouthwestBlue'] = __loadTransposed('lib/images/cornerBlue.gif', PI.FLIP_TOP_BOTTOM)
    images['cornerSouthwestRed'] = __loadTransposed('lib/images/cornerRed.gif', PI.FLIP_TOP_BOTTOM)

    images['cornerSoutheast'] = __loadTransposed('lib/images/corner.gif', PI.ROTATE_180)
    images['cornerSoutheastBlue'] = __loadTransposed('lib/images/cornerBlue.gif', PI.ROTATE_180)
    images['cornerSoutheastRed'] = __loadTransposed('lib/images/cornerRed.gif', PI.ROTATE_180)

    return images


def __load(gif):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image)


def __loadTransposed(gif, transposition):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image.transpose(transposition))
