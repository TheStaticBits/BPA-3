import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.tileset import Tileset


class Building(Entity):
    """ All buildings inherit from this base building class
        Handles placing of buildings, size/hitboxes, etc. """

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
        buildingTileSize: Vect = Vect(cls.getData(type)["size"])

        # Test if out of range of tiles
        if (tilePos.x + buildingTileSize.x > tileset.getTileSize().x or
                tilePos.y + buildingTileSize.y > tileset.getTileSize().y or
                tilePos.x < 0 or tilePos.y < 0):
            return False

        # Iterate through the tiles the building would occupy
        for y in range(buildingTileSize.y):
            for x in range(buildingTileSize.x):
                if tileset.isOccupied(tilePos + Vect(x, y)):
                    return False

        return True

    @classmethod
    def getData(cls, type: str) -> dict:
        return cls.BUILDINGS_DATA[type]

    def __init__(self, tileset: Tileset,
                 type: str, tilePos: Vect = Vect()) -> None:
        """ Setup initial position, animation, and
            set tiles where the building is to occupied """

        super().__init__(self.getData(type)["anim"], __name__,
                         tilePos * Tileset.TILE_SIZE)

        self.type = type

        self.place(tileset, tilePos)

    def place(self, tileset: Tileset, tilePos: Vect) -> None:
        """ Places the building on the tileset,
            setting occupied tiles to True """
        buildingTileSize: Vect = Vect(self.getData(self.type)["size"])

        # Iterate through the tiles the building would occupy
        # setting occupied to True
        for y in range(buildingTileSize.y):
            for x in range(buildingTileSize.x):
                tileset.setOccupied(tilePos + Vect(x, y))
