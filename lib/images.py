from PIL import Image as PI
from PIL import ImageTk


images = None


def getImageByColor(color, highlight):
    global images
    if images is None:
        images = __loadImages()
    highlightDescriptor = ''
    if highlight:
        highlightDescriptor = 'Highlight'
    return images[color + highlightDescriptor]


# Returns the image that goes at the row and colum in Pente
def getImage(row, column, highlight):
    global images
    return getBeadImage(row, column, 'Open', highlight)


# Returns the image that goes at the row and colum in Pente
# with a bead played in that location
def getBeadImage(row, column, color, highlight):
    global images

    # Singleton lazy load all the images
    if images is None:
        __loadImages()

    highlightDescriptor = ''
    if highlight:
        highlightDescriptor = 'Highlight'

    return images[color + '_' + __getKey(row, column) + highlightDescriptor]


def __getKey(row, column):
    global images

    # NOTE: These are very order dependent, do not move them around

    # Diamonds
    if (row == 6 and column == 6) or (row == 6 and column == 12) or (row == 12 and column == 6) or (row == 12 and column == 12):
        return 'Diamond'
    if (row == 3 and column == 3) or (row == 3 and column == 15) or (row == 15 and column == 3) or (row == 15 and column == 15):
        return 'Diamond'
    if (row == 3 and column == 9) or (row == 15 and column == 9):
        return 'Diamond_Bold1_North'
    if (row == 9 and column == 3) or (row == 9 and column == 15):
        return 'Diamond_Bold1_East'
    if row == 9 and column == 9:
        return 'Diamond_Bold2'

    # Handle the Corners
    if row == 0 and column == 0:
        return 'Corner_Northwest'
    if row == 0 and column == 18:
        return 'Corner_Northeast'
    if row == 18 and column == 0:
        return 'Corner_Southwest'
    if row == 18 and column == 18:
        return 'Corner_Southeast'

    # Bold T Intersections (outer edge)
    if row == 0 and column == 9:
        return 'TIntersection_Bold2_North'
    if row == 9 and column == 0:
        return 'TIntersection_Bold2_West'
    if row == 9 and column == 18:
        return 'TIntersection_Bold2_East'
    if row == 18 and column == 9:
        return 'TIntersection_Bold2_South'

    # T Intersections (outer edge)
    if row == 0:
        return 'TIntersection_Bold1_North'
    if column == 0:
        return 'TIntersection_Bold1_West'
    if column == 18:
        return 'TIntersection_Bold1_East'
    if row == 18:
        return 'TIntersection_Bold1_South'

    # Bold midway Vertical and Horizontal lines
    if column == 9:
        return 'Intersection_Bold1_North'
    if row == 9:
        return 'Intersection_Bold1_East'

    # Default Intersection
    return 'Intersection'


def __loadImages():
    global images
    images = {}

    images['Blue'] = __load('lib/images/Blue.gif')
    images['BlueHighlight'] = __load('lib/images/BlueHighlight.gif')
    images['Red'] = __load('lib/images/Red.gif')
    images['RedHighlight'] = __load('lib/images/RedHighlight.gif')

    types = [
        {
            "name": "Diamond",
            "directions": None
        },
        {
            "name": "Diamond_Bold1",
            "directions": {
                "North": None,
                "East": PI.ROTATE_270
            }
        },
        {
            "name": "Diamond_Bold2",
            "directions": None
        },
        {
            "name": "Corner",
            "directions": {
                "Northwest": None,
                "Northeast": PI.FLIP_LEFT_RIGHT,
                "Southwest": PI.FLIP_TOP_BOTTOM,
                "Southeast": PI.ROTATE_180
            }
        },
        {
            "name": "Intersection",
            "directions": None
        },
        {
            "name": "Intersection_Bold1",
            "directions": {
                "North": None,
                "East": PI.ROTATE_270
            }
        },
        {
            "name": "TIntersection_Bold1",
            "directions": {
                "North": None,
                "South": PI.FLIP_TOP_BOTTOM,
                "East": PI.ROTATE_270,
                "West": PI.ROTATE_90
            }
        },
        {
            "name": "TIntersection_Bold2",
            "directions": {
                "North": None,
                "South": PI.FLIP_TOP_BOTTOM,
                "East": PI.ROTATE_270,
                "West": PI.ROTATE_90
            }
        },
    ];


    for type in types:
        if type["directions"] is None:
            __loadImageGroup(type, '', None)
        else:
            for direction in type["directions"].keys():
                __loadImageGroup(type, '_' + direction, type["directions"][direction])


def __loadImageGroup(type, direction, rotation):
    global images
    colors = [ 'Open', 'Blue', 'Red' ]
    for color in colors:
        if rotation is None:
            key = color + '_' + type["name"] + direction
            image = color + '_' + type["name"] + '.gif'
            # print(key + ': ' + image)
            images[key] = __load('lib/images/' + image)
            key = color + '_' + type["name"] + direction + 'Highlight'
            image = color + '_' + type["name"] + 'Highlight.gif'
            # print(key + ': ' + image)
            images[key] = __load('lib/images/' + image)
        else:
            key = color + '_' + type["name"] + direction
            image = color + '_' + type["name"] + '.gif'
            # print(key + ': ' + image)
            images[key] = __loadTransposed('lib/images/' + image, rotation)
            key = color + '_' + type["name"] + direction + 'Highlight'
            image = color + '_' + type["name"] + 'Highlight.gif'
            # print(key + ': ' + image)
            images[key] = __loadTransposed('lib/images/' + image, rotation)


def __load(gif):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image)


def __loadTransposed(gif, transposition):
    image = PI.open(gif)
    return ImageTk.PhotoImage(image.transpose(transposition))
