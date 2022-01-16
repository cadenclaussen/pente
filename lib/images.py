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
def getImage(x, y, highlight):
    global images
    return getBeadImage(x, y, 'Open', highlight)


# Returns the image that goes at the row and colum in Pente
# with a bead played in that location
def getBeadImage(x, y, color, highlight):
    global images

    # Singleton lazy load all the images
    if images is None:
        __loadImages()

    highlightDescriptor = ''
    if highlight:
        highlightDescriptor = 'Highlight'

    return images[color + '_' + __getKey(x, y) + highlightDescriptor]


def __getKey(x, y):
    global images

    # NOTE: These are very order dependent, do not move them around

    # Diamonds
    if (y == 6 and x == 6) or (y == 6 and x == 12) or (y == 12 and x == 6) or (y == 12 and x == 12):
        return 'Diamond'
    if (y == 3 and x == 3) or (y == 3 and x == 15) or (y == 15 and x == 3) or (y == 15 and x == 15):
        return 'Diamond'
    if (y == 3 and x == 9) or (y == 15 and x == 9):
        return 'Diamond_Bold1_North'
    if (y == 9 and x == 3) or (y == 9 and x == 15):
        return 'Diamond_Bold1_East'
    if y == 9 and x == 9:
        return 'Diamond_Bold2'

    # Handle the Corners
    if y == 0 and x == 0:
        return 'Corner_Northwest'
    if y == 0 and x == 18:
        return 'Corner_Northeast'
    if y == 18 and x == 0:
        return 'Corner_Southwest'
    if y == 18 and x == 18:
        return 'Corner_Southeast'

    # Bold T Intersections (outer edge)
    if y == 0 and x == 9:
        return 'TIntersection_Bold2_North'
    if y == 9 and x == 0:
        return 'TIntersection_Bold2_West'
    if y == 9 and x == 18:
        return 'TIntersection_Bold2_East'
    if y == 18 and x == 9:
        return 'TIntersection_Bold2_South'

    # T Intersections (outer edge)
    if y == 0:
        return 'TIntersection_Bold1_North'
    if x == 0:
        return 'TIntersection_Bold1_West'
    if x == 18:
        return 'TIntersection_Bold1_East'
    if y == 18:
        return 'TIntersection_Bold1_South'

    # Bold midway Vertical and Horizontal lines
    if x == 9:
        return 'Intersection_Bold1_North'
    if y == 9:
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
    images['Green'] = __load('lib/images/Green.gif')
    images['GreenHighlight'] = __load('lib/images/GreenHighlight.gif')

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
    colors = [ 'Open', 'Blue', 'Red', 'Green' ]
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
