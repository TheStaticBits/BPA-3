import logging
import os

import src.utility.utility as util
from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window


class Tileset:
    """ Stores tiles along with interactable entities
        such as buildings and trees aside from buildings """
    log = logging.getLogger(__name__)

    @classmethod  # static function
    def loadStatic(cls, constants: dict) -> None:
        """ Loads metadata about the tilesets from the constants file
            into several static variables """
        # Static data about tilesets loaded from constants.json
        cls.TILE_SIZE: Vect = (
            Vect(constants["tileset"]["tileSize"]) * Image.SCALE
        )

        # FILE INFO:

        # Map folder containing folders for each map
        cls.MAPS_FOLDER: str = constants["tileset"]["mapsFolder"]
        # File inside each map folder for map data (JSON)
        cls.JSON_FILE: str = constants["tileset"]["jsonFile"]
        # File for map data (txt)
        cls.MAP_FILE: str = constants["tileset"]["mapFile"]

        # Tileset data loaded from JSON file
        cls.TILESET_DATA: dict = util.loadJSON(
            constants["tileset"]["tilesFile"]
        )

    def __init__(self, mapFolderName: str) -> None:
        """ Load tileset information and tiles """

        # Entire map/tileset image
        self.tiles: Image = None

        # 2D array for occupied tiles (for things like placing buildings)
        self.occupiedTiles: list[list[bool]] = []

        # Load map info
        self.loadMapData(os.path.join(self.MAPS_FOLDER, mapFolderName,
                                      self.JSON_FILE))

        self.generateMapImg(os.path.join(self.MAPS_FOLDER, mapFolderName,
                                         self.MAP_FILE))

    def loadMapData(self, dataPath: dict) -> None:
        """ Loads the JSON containing map metadata and vars from it """

        self.data: dict = util.loadJSON(dataPath)
        self.playerStart = Vect(self.data["playerSpawn"]) * self.TILE_SIZE

    def generateMapImg(self, mapPath: str) -> None:
        """ Generates the tiles based on the chars in the map data """

        mapData: str = util.loadFile(mapPath)
        splitData: list[str] = mapData.split("\n")

        self.size: Vect = Vect(len(splitData[0]), len(splitData))

        surfSize = Vect(len(splitData[0]) * self.TILE_SIZE.x,
                        len(splitData) * self.TILE_SIZE.y)

        # Create empty tileset image based on the tiledata
        self.tiles = Image.makeEmpty(surfSize, scale=True)

        # Create Tile objects for every char in the map data
        for y, row in enumerate(splitData):  # Rows
            # Add a row of False to occupiedTiles
            self.occupiedTiles.append([False] * len(row))

            for x, tileChar in enumerate(row):  # Columns
                # Gets position of the tile in pixels
                pos: Vect = Vect(x, y) * self.TILE_SIZE

                # Load image and draw to tiles image at the current pos
                tileImg = Image(self.TILESET_DATA[tileChar])
                self.tiles.render(tileImg, pos)

    def update(self, window: Window) -> None:
        """ Will be used to update anything in the tileset
            with animations in the future """

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders tileset image """
        surface.render(self.tiles, offset)

    def testRangeOccupied(self, startTile: Vect, tileRange: Vect) -> bool:
        """ Tests if a range of tiles has at least one tile occupied """
        for y in range(tileRange.y):
            for x in range(tileRange.x):
                if self.isOccupied(startTile + Vect(x, y)):
                    return True

        return False

    def setRangeOccupied(self, startTile: Vect, tileRange: Vect,
                         state: bool = True) -> None:
        """ Sets the occupied status of a range of tiles """
        for y in range(tileRange.y):
            for x in range(tileRange.x):
                self.setOccupied(startTile + Vect(x, y), state)

    # Getters
    def getPlayerStart(self) -> Vect:
        return self.playerStart

    def isOccupied(self, tilePos: Vect) -> bool:
        """ Returns whether or not a tile is occupied """
        return self.occupiedTiles[tilePos.y][tilePos.x]

    def getTileSize(self) -> Vect: return self.size
    def getSize(self) -> Vect: return self.size * self.TILE_SIZE
    def getData(self) -> dict: return self.data

    # Setters
    def setOccupied(self, tilePos: Vect, state: bool = True) -> None:
        """ Sets the occupied status of a tile """
        self.occupiedTiles[tilePos.y][tilePos.x] = state
