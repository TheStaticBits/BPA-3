import pygame
import logging
import os

import src.utility.utility as util
from src.utility.vector import Vect
from src.window import Window


class Tileset:
    """ Stores tiles along with interactable entities
        such as buildings and trees aside from buildings """

    # Tile images cache { path: pygame.Surface }
    tileImages: dict = {}

    @classmethod  # static function
    def loadStatic(cls, constants: dict) -> None:
        """ Loads metadata about the tilesets from the constants file
            into several static variables """
        # Static data about tilesets loaded from constants.json
        cls.TILE_SIZE: Vect = (
            Vect(constants["tileset"]["tileSize"]) * Window.getImgScale()
        )

        # FILE INFO:

        # Map folder containing folders for each map
        cls.MAPS_FOLDER: str = constants["tileset"]["mapsFolder"]
        # File inside each map folder for map data (JSON)
        cls.JSON_FILE: str = constants["tileset"]["jsonFile"]
        # File for entities data (txt)
        cls.ENTITIES_FILE: str = constants["tileset"]["entitiesFile"]
        # File for map data (txt)
        cls.MAP_FILE: str = constants["tileset"]["mapFile"]

        # Tileset data loaded from JSON file
        cls.TILESET_DATA: dict = util.loadJSON(
            constants["tileset"]["tilesFile"]
        )

    def __init__(self, mapFolderName: str) -> None:
        """ Load tileset information and tiles"""

        self.log = logging.getLogger(__name__)

        # Entire map/tileset image
        self.tiles: pygame.Surface = None

        # 2D array for occupied tiles (for things like placing buildings)
        self.occupiedTiles: list[list[bool]] = []

        # Load map info
        self.loadMapData(os.path.join(self.MAPS_FOLDER, mapFolderName,
                                      self.JSON_FILE))

        self.loadEntities(os.path.join(self.MAPS_FOLDER, mapFolderName,
                                       self.ENTITIES_FILE))

        self.loadFromText(os.path.join(self.MAPS_FOLDER, mapFolderName,
                                       self.MAP_FILE))

    def loadMapData(self, dataPath: dict) -> None:
        """ Loads the JSON containing map metadata and vars from it """

        mapData: dict = util.loadJSON(dataPath)
        self.PLAYER_START = Vect(mapData["playerSpawn"]) * self.TILE_SIZE

    def loadEntities(self, entitiesPath: str) -> None:
        """ Loads any minable entities TO BE IMPLEMENTED (or removed) """
        pass

    def loadFromText(self, mapPath: str) -> None:
        """ Generates the tiles based on the chars in the map data """

        mapData: str = util.loadFile(mapPath)
        splitData: list[str] = mapData.split("\n")

        self.size: Vect = Vect(len(splitData[0]), len(splitData))

        # Create empty tileset image based on the tiledata
        self.tiles = pygame.Surface((len(splitData[0]) * self.TILE_SIZE.x,
                                     len(splitData) * self.TILE_SIZE.y),
                                    pygame.DOUBLEBUF | pygame.HWSURFACE)

        # Create Tile objects for every char in the map data
        for y, row in enumerate(splitData):  # Iterate through rows

            # Add a row of False to occupiedTiles
            self.occupiedTiles.append([False] * len(row))

            # Iterate through columns
            for x, tileChar in enumerate(row):

                # Gets position of the tile in pixels
                pos: Vect = Vect(x, y) * self.TILE_SIZE

                # Load tile image
                tileImg = self.getTileImg(self.TILESET_DATA[tileChar])

                # Draw to the tileset image
                self.tiles.blit(tileImg, pos.toTuple())

    def getTileImg(self, path: str) -> pygame.Surface:
        """ Gets the tile image from the cache
            or loads it if it has not been loaded previously """
        if path not in self.tileImages:
            self.log.info(f"Loading tile image at {path}")
            self.tileImages[path] = Window.loadImg(path)

        return self.tileImages[path]

    def update(self, window: Window) -> None:
        """ Will be used to update anything in the tileset
            with animations in the future """
        pass

    def render(self, window: Window, offset: Vect = Vect()) -> None:
        """ Renders tileset image """
        window.render(self.tiles, offset)

        # Draw red square over tiles that are occupied (debugging)
        for y, row in enumerate(self.occupiedTiles):
            for x, occupied in enumerate(row):
                if not occupied:
                    continue

                window.drawRect(Vect(x, y) * self.TILE_SIZE + offset + Vect(3),
                                self.TILE_SIZE - Vect(6), (255, 0, 0))

    def testRangeOccupied(self, startTile: Vect, tileRange: Vect) -> bool:
        """ Tests if a range of tiles has at least one tile occupied """
        for y in range(tileRange.y):
            for x in range(tileRange.x):
                if self.isOccupied(startTile + Vect(x, y)):
                    return True

        return False

    def setRangeOccupied(self, startTile: Vect, tileRange: Vect) -> None:
        """ Sets the occupied status of a range of tiles """
        for y in range(tileRange.y):
            for x in range(tileRange.x):
                self.setOccupied(startTile + Vect(x, y))

    # Getters
    def getPlayerStart(self) -> Vect:
        return self.PLAYER_START

    def isOccupied(self, tilePos: Vect) -> bool:
        """ Returns whether or not a tile is occupied """
        return self.occupiedTiles[tilePos.y][tilePos.x]

    def getTileSize(self) -> Vect: return self.size
    def getSize(self) -> Vect: return self.size * self.TILE_SIZE

    # Setters
    def setOccupied(self, tilePos: Vect) -> None:
        """ Sets the occupied status of a tile """
        self.occupiedTiles[tilePos.y][tilePos.x] = True
