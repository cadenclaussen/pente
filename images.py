from PIL import Image as PI
from PIL import ImageTk


images = None


def getTileByColor(color, highlight):
    global images
    if images is None:
        images = loadTiles()
    tileSuffix = ''
    if highlight:
        tileSuffix = '_Highlighted'
    return images[color + tileSuffix]


def getOpenTile(x, y):
    return getTile(x, y, 'Open', None)

def getOpenTileOffense(x, y):
    return getTile(x, y, 'Open', 'Offense')

def getOpenTileDefense(x, y):
    return getTile(x, y, 'Open', 'Defense')

def getBeadTile(x, y, color):
    return getTile(x, y, color, None)

def getBeadTileHighlight(x, y, color):
    return getTile(x, y, color, 'Highlighted')



def getTile(x, y, tilePrefix, tileSuffix):
    global images

    # Singleton lazy load all the images
    if images is None:
        loadTiles()

    if tileSuffix is None:
        tileSuffix = ''
    else:
        tileSuffix = '_' + tileSuffix

    # Prefixes: Open, Blue, Red, Green
    # Tile Name and Direction: Intersection, Diamond_Bold2, Diamond_Bold1_North
    # Tile Suffix: Offense, Defense, Highlighted
    return images[tilePrefix + '_' + getTileNameAndDirection(x, y) + tileSuffix]


def getTileNameAndDirection(x, y):
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


def loadTiles():
    global images
    images = {}

    images['Blue'] = loadTile('Blue.gif', None)
    images['BlueHighlight'] = loadTile('Blue_Highlighted.gif', None)
    images['Red'] = loadTile('Red.gif', None)
    images['RedHighlight'] = loadTile('Red_Highlighted.gif', None)
    images['Green'] = loadTile('Green.gif', None)
    images['GreenHighlight'] = loadTile('Green_Highlighted.gif', None)

    tileGroups = [
        {
            'name': 'Diamond',
        },
        {
            'name': 'Diamond_Bold1',
            'directions': {
                'North': None,
                'East': PI.ROTATE_270
            }
        },
        {
            'name': 'Diamond_Bold2',
        },
        {
            'name': 'Corner',
            'directions': {
                'Northwest': None,
                'Northeast': PI.FLIP_LEFT_RIGHT,
                'Southwest': PI.FLIP_TOP_BOTTOM,
                'Southeast': PI.ROTATE_180
            }
        },
        {
            'name': 'Intersection',
        },
        {
            'name': 'Intersection_Bold1',
            'directions': {
                'North': None,
                'East': PI.ROTATE_270
            }
        },
        {
            'name': 'TIntersection_Bold1',
            'directions': {
                'North': None,
                'South': PI.FLIP_TOP_BOTTOM,
                'East': PI.ROTATE_270,
                'West': PI.ROTATE_90
            }
        },
        {
            'name': 'TIntersection_Bold2',
            'directions': {
                'North': None,
                'South': PI.FLIP_TOP_BOTTOM,
                'East': PI.ROTATE_270,
                'West': PI.ROTATE_90
            }
        },
    ];

    for tileGroup in tileGroups:
        if 'directions' not in tileGroup:
            loadTileGroup(tileGroup['name'], '', None)
            continue

        for directionKey in tileGroup['directions'].keys():
            loadTileGroup(tileGroup['name'], '_' + directionKey, tileGroup['directions'][directionKey])


def loadTileGroup(tileName, directionKey, direction):
    global images
    for tilePrefix in [ 'Open', 'Blue', 'Red', 'Green' ]:
        # Load images, examples:
        # - Open_Intersection     -> Open_Intersection.gif
        # - Blue_Intersection     -> Blue_Intersection.gif
        # - Open_Corner_Northwest -> Open_Corner.gif
        # - Open_Corner_Northeast -> Open_Corner.gif (Northeast)
        # - Blue_Corner_Northwest -> Blue_Corner.gif
        # - Blue_Corner_Northeast -> Blue_Corner.gif (Northeast)
        key = tilePrefix + '_' + tileName + directionKey
        image = tilePrefix + '_' + tileName + '.gif'
        images[key] = loadTile(image, direction)

        for tileSuffix in [ 'Offense', 'Defense', 'Highlighted' ]:
            if (tilePrefix == 'Open' and tileSuffix == 'Highlighted') or (tilePrefix != 'Open' and tileSuffix != 'Highlighted'):
                continue

            # Load images, examples:
            # - Open_Intersection_Offense         -> Open_Intersection_Offense.gif
            # - Open_Intersection_Defense         -> Open_Intersection_Defense.gif
            # - Blue_Intersection_Highlighted     -> Blue_Intersection_Highlighted.gif
            # - Blue_Intersection_Highlighted     -> Blue_Intersection_Highlighted.gif
            # - Blue_Corner_Northwest_Highlighted -> Blue_Corner_Highlighted.gif
            # - Blue_Corner_Northeast_Highlighted -> Blue_Corner_Highlighted.gif (Northeast)
            key = tilePrefix + '_' + tileName + directionKey + '_' + tileSuffix
            image = tilePrefix + '_' + tileName + '_' + tileSuffix + '.gif'
            images[key] = loadTile(image, direction)


def loadTile(imageFile, direction):
    image = PI.open('images/' + imageFile)
    if direction is None:
        return ImageTk.PhotoImage(image)
    return ImageTk.PhotoImage(image.transpose(direction))
