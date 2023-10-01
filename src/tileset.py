import logging

import src.utility.utility as util
from src.entities.tile import Tile
from src.utility.vector import Vect
from src.window import Window

class Tileset:
    """ Stores tiles along with interactable entities
        such as buildings and trees aside from buildings """
    
    # Static data about tilesets loaded from constants.json
    TILE_SIZE: Vect = None

    # File info
    MAPS_FOLDER: str = None # Map folder containing folders for each map (eg data/maps)
    JSON_FILE: str = None # File inside each map folder for map data (JSON)
    ENTITIES_FILE: str = None # File for entities data (txt)
    MAP_FILE: str = None # File for map data (txt)

    # Tile data
    TILESET_DATA: dict = None # Tileset data loaded from JSON file


    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads metadata about the tilesets from the constants file
            into several static variables """
        
        cls.TILE_SIZE = Vect(constants["tileset"]["tileSize"])

        cls.MAPS_FOLDER = constants["tileset"]["mapsFolder"]
        cls.JSON_FILE = constants["tileset"]["jsonFile"]
        cls.ENTITIES_FILE = constants["tileset"]["entitiesFile"]
        cls.MAP_FILE = constants["tileset"]["mapFile"]

        cls.TILESET_DATA = util.loadJSON(constants["tileset"]["tilesFile"])
    

    def __init__(self, mapFolderName: str) -> None:
        """ Load tileset information and tiles"""

        self.log = logging.getLogger(__name__)

        # List of tiles
        self.tiles: list[list[Tile]] = []

        containingFolder: str = f"{self.MAPS_FOLDER}/{mapFolderName}"

        # Load map info
        self.loadMapData(f"{containingFolder}/{self.JSON_FILE}")
        self.loadEntities(f"{containingFolder}/{self.ENTITIES_FILE}")
        self.loadFromText(f"{containingFolder}/{self.MAP_FILE}")
    

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

        # Create Tile objects for every char in the map data
        for y, row in enumerate(splitData): # Iterate through rows
            self.tiles.append([]) # add row

            for x, tileChar in enumerate(row): # Iterate through columns

                pos: Vect = Vect(x, y) * self.TILE_SIZE

                # Generate Tile objects
                # Occupied is set to False initially,
                # will be set to true when loading other entities or buildings
                tileObj: Tile = Tile(pos, False, self.TILESET_DATA[tileChar])
                
                # Append to the last row in the list
                self.tiles[-1].append(tileObj)

    
    def update(self, window: Window) -> None:
        """ Updates all tiles' animations """

        # This annotates the type of the for loop iterator
        # since you cannot annotate it inside the for loop
        row: list[Tile]
        for row in self.tiles:
            tile: Tile
            for tile in row:
                tile.update(window)
    

    def render(self, window: Window, offset: Vect=Vect()) -> None:
        """ Renders all tiles """
        
        row: list[Tile]
        for row in self.tiles:
            tile: Tile
            for tile in row:
                tile.render(window, offset=offset)

    
    # Getters
    def getPlayerStart(self) -> Vect:
        return self.PLAYER_START