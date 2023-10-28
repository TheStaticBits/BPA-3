import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.tileset import Tileset
from src.window import Window


class BaseBuilding(Entity):
    """ All buildings inherit from this base building class
        Handles placing of buildings, size/hitboxes, etc.
        Inherits from Entity class for animation and position handling. """

    # Static functions
    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the buildings data JSON file """
        # Building JSON data file (data/buildings.json)
        cls.BUILDINGS_DATA: str = util.loadJSON(
            constants["buildings"]["jsonPath"]
        )

    @classmethod
    def testPlacement(cls, type: str, tilePos: Vect, tileset: Tileset) -> bool:
        """ Tests if the tiles in the tileset
            at tilePos are occupied or not """
        data: dict = cls.BUILDINGS_DATA[type]

        buildingTileSize = Vect(data["size"])

        # Test if out of range of tiles
        if (tilePos.x + buildingTileSize.x > tileset.getTileSize().x or
                tilePos.y + buildingTileSize.y > tileset.getTileSize().y or
                tilePos.x < 0 or tilePos.y < 0):
            return False

        # Test if any tiles are occupied
        return not tileset.testRangeOccupied(tilePos, buildingTileSize)

    def __init__(self, type: str, tileset: Tileset, tilePos: Vect) -> None:
        """ Setup initial position, animation, and
            set tiles where the building is to occupied """

        self.type = type

        super().__init__(self.getData()["anim"], __name__,
                         tilePos * Tileset.TILE_SIZE)

        self.place(tileset, tilePos)

    def onRemove(self) -> None:
        """ Overriden in subclasses.
            Called on building removal. """

    def update(self, window: Window) -> None:
        """ Override in subclasses. """
        super().update(window)

    def place(self, tileset: Tileset, tilePos: Vect) -> None:
        """ Places the building on the tileset,
            setting occupied tiles to True """
        buildingTileSize: Vect = Vect(self.getData()["size"])

        # Sets the range of tiles that the building takes up to occupied
        # so no other building can be placed there
        tileset.setRangeOccupied(tilePos, buildingTileSize)

    def getData(self) -> dict:
        return self.BUILDINGS_DATA[self.type]

    @classmethod
    def getDataFrom(cls, type: str) -> dict:
        return cls.BUILDINGS_DATA[type]
