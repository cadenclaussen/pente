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
def getBeadImage(row, column, currentPlayer):
    global images

    # Singleton lazy load all the images
    if images == {}:
        images = __loadImages()

    if currentPlayer == 0:
        return images[__getKey(row, column) + "Blue"]
    return images[__getKey(row, column) + "Red"]


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

    images['center'] = __load('view/images/center.gif')
    images['centerBlue'] = __load('view/images/centerBlue.gif')
    images['centerRed'] = __load('view/images/centerRed.gif')

    images['diamond'] = __load('view/images/diamond.gif')
    images['diamondBlue'] = __load('view/images/plusblue.gif')
    images['diamondRed'] = __load('view/images/plusred.gif')

    images['diamondVertical'] = __load('view/images/diamondvertical.gif')
    images['diamondVerticalBlue'] = __load('view/images/verticalblue.gif')
    images['diamondVerticalRed'] = __load('view/images/verticalred.gif')

    images['diamondHorizontal'] = __loadTransposed('view/images/diamondvertical.gif', PI.ROTATE_90)
    images['diamondHorizontalBlue'] = __loadTransposed('view/images/verticalblue.gif', PI.ROTATE_90)
    images['diamondHorizontalRed'] = __loadTransposed('view/images/verticalred.gif', PI.ROTATE_90)

    images['plus'] = __load('view/images/plus.gif')
    images['plusBlue'] = __load('view/images/plusblue.gif')
    images['plusRed'] = __load('view/images/plusred.gif')

    images['vertical'] = __load('view/images/vertical.gif')
    images['verticalBlue'] = __load('view/images/verticalblue.gif')
    images['verticalRed'] = __load('view/images/verticalred.gif')

    images['horizontal'] = __loadTransposed('view/images/vertical.gif', PI.ROTATE_90)
    images['horizontalBlue'] = __loadTransposed('view/images/verticalblue.gif', PI.ROTATE_90)
    images['horizontalRed'] = __loadTransposed('view/images/verticalred.gif', PI.ROTATE_90)

    images['tNorth'] = __load('view/images/t.gif')
    images['tNorthBlue'] = __load('view/images/tblue.gif')
    images['tNorthRed'] = __load('view/images/tred.gif')

    images['tSouth'] = __loadTransposed('view/images/t.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBlue'] = __loadTransposed('view/images/tblue.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthRed'] = __loadTransposed('view/images/tred.gif', PI.FLIP_TOP_BOTTOM)

    images['tEast'] = __loadTransposed('view/images/t.gif', PI.ROTATE_270)
    images['tEastBlue'] = __loadTransposed('view/images/tblue.gif', PI.ROTATE_270)
    images['tEastRed'] = __loadTransposed('view/images/tred.gif', PI.ROTATE_270)

    images['tWest'] = __loadTransposed('view/images/t.gif', PI.ROTATE_90)
    images['tWestBlue'] = __loadTransposed('view/images/tblue.gif', PI.ROTATE_90)
    images['tWestRed'] = __loadTransposed('view/images/tred.gif', PI.ROTATE_90)

    images['tNorthBold'] = __load('view/images/tbold.gif')
    images['tNorthBoldBlue'] = __load('view/images/tboldblue.gif')
    images['tNorthBoldRed'] = __load('view/images/tboldred.gif')

    images['tSouthBold'] = __loadTransposed('view/images/tbold.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBoldBlue'] = __loadTransposed('view/images/tboldblue.gif', PI.FLIP_TOP_BOTTOM)
    images['tSouthBoldRed'] = __loadTransposed('view/images/tboldred.gif', PI.FLIP_TOP_BOTTOM)

    images['tEastBold'] = __loadTransposed('view/images/tbold.gif', PI.ROTATE_270)
    images['tEastBoldBlue'] = __loadTransposed('view/images/tboldblue.gif', PI.ROTATE_270)
    images['tEastBoldRed'] = __loadTransposed('view/images/tboldred.gif', PI.ROTATE_270)

    images['tWestBold'] = __loadTransposed('view/images/tbold.gif', PI.ROTATE_90)
    images['tWestBoldBlue'] = __loadTransposed('view/images/tboldblue.gif', PI.ROTATE_90)
    images['tWestBoldRed'] = __loadTransposed('view/images/tboldred.gif', PI.ROTATE_90)

    images['cornerNorthwest'] = __load('view/images/corner.gif')
    images['cornerNorthwestBlue'] = __load('view/images/cornerBlue.gif')
    images['cornerNorthwestRed'] = __load('view/images/cornerRed.gif')

    images['cornerNortheast'] = __loadTransposed('view/images/corner.gif', PI.FLIP_LEFT_RIGHT)
    images['cornerNortheastBlue'] = __loadTransposed('view/images/cornerBlue.gif', PI.FLIP_LEFT_RIGHT)
    images['cornerNortheastRed'] = __loadTransposed('view/images/cornerRed.gif', PI.FLIP_LEFT_RIGHT)

    images['cornerSouthwest'] = __loadTransposed('view/images/corner.gif', PI.FLIP_TOP_BOTTOM)
    images['cornerSouthwestBlue'] = __loadTransposed('view/images/cornerBlue.gif', PI.FLIP_TOP_BOTTOM)
    images['cornerSouthwestRed'] = __loadTransposed('view/images/cornerRed.gif', PI.FLIP_TOP_BOTTOM)

    images['cornerSoutheast'] = __loadTransposed('view/images/corner.gif', PI.ROTATE_180)
    images['cornerSoutheastBlue'] = __loadTransposed('view/images/cornerBlue.gif', PI.ROTATE_180)
    images['cornerSoutheastRed'] = __loadTransposed('view/images/cornerRed.gif', PI.ROTATE_180)

    return images


def __load(gif):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image)


def __loadTransposed(gif, transposition):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image.transpose(transposition))
