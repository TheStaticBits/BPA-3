import pygame
import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.tileset import Tileset
from src.window import Window
from src.entities.player import Player
from src.utility.image import Image


class BaseBuilding(Entity):
    """ All buildings inherit from this base building class
        Handles placing of buildings, size/hitboxes, etc.
        Inherits from Entity class for animation and position handling. """

    # Static functions
    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the buildings data JSON file """
        # Building JSON data file (data/buildings.json)
        cls.BUILDINGS_DATA: dict = util.loadJSON(
            constants["buildings"]["jsonPath"]
        )

        cls.BUILD_REACH: int = constants["buildings"]["buildReachTiles"] \
            * Tileset.TILE_SIZE.x

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

    def __init__(self, type: str) -> None:
        """ Setup initial position, animation, and
            set tiles where the building is to occupied """

        self.type: str = type
        self.placing: bool = True
        self.placable: bool = False

        super().__init__(self.getData()["anim"], __name__, Tileset.TILE_SIZE)

    def onRemove(self) -> None:
        """ Overriden in subclasses.
            Called on building removal. """

    def onPlace(self) -> None:
        """ Overriden in subclasses.
            Called on building placement. """

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player) -> None:
        """ Updates the building by following the cursor and testing placement
            and updating animation if not placing"""
        if self.placing:
            self.followCursor(window, camOffset, tileset, player)
            self.testPlace(window, tileset)
        else:  # update animation:
            super().update(window)

    def followCursor(self, window: Window, camOffset: Vect,
                     tileset: Tileset, player: Player) -> None:
        """ Moves to cursor and tests if the building can be placed
            Also limits the cursor position to a range around the player """
        # Get cursor position and convert to position on the tileset
        mousePos: Vect = window.getMousePos() + camOffset

        # Get player center position
        playerPos: Vect = player.getCenterPos()

        # Find distance between player and cursor
        dist: Vect = mousePos.dist(playerPos)

        if dist > self.BUILD_REACH:
            # Cursor is too far from player, clamp to max distance

            # Get angle between player and cursor
            angle: float = mousePos.angle(playerPos)

            # Get distance from angle and max distance
            dist: Vect = Vect.distFromAngle(angle, self.BUILD_REACH)

            # Set mousePos to the new position
            mousePos = playerPos + dist

        # Offset by half the building size
        mousePos -= super().getSize() / 2

        # Calculate tile position of the cursor
        self.tilePos = mousePos / Tileset.TILE_SIZE
        self.tilePos = self.tilePos.floor()

        # Clamp to the tile map so it doesn't go over the edge
        self.tilePos.clamp(Vect(0, 0), tileset.getTileSize() - Vect(1, 1))

        # Set position to new self.tilePos
        super().setPos(self.tilePos * Tileset.TILE_SIZE)

    def testPlace(self, window: Window, tileset: Tileset) -> None:
        """ Tests if the building can be placed and places it """
        self.placable = self.testPlacement(self.type, self.tilePos, tileset)

        if self.placable and window.getMouseJustPressed("left"):
            self.placing = False

            buildingTileSize: Vect = Vect(self.getData()["size"])

            # Sets the range of tiles that the building takes up to occupied
            # so no other building can be placed there
            tileset.setRangeOccupied(self.tilePos, buildingTileSize)

            self.onPlace()

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Render with tints if placing """
        if self.placing:
            # Create a new surface the size of the building image
            surf = pygame.Surface(super().getSize().toTuple(), pygame.SRCALPHA)
            img = Image(surf=surf, scale=False)

            # Render the current animation frame on the new surface
            super().render(img, -super().getPos())
            img.setAlpha(150)

            # Tint red if not placeable
            if not self.placable:
                img.fill(255, 0, 0, 150)

            # Draw the new tinted surface to the screen
            surface.render(img, super().getPos() + offset)

        else:
            super().render(surface, offset)

    # Getters
    def getData(self) -> dict:
        return self.BUILDINGS_DATA[self.type]

    def isPlacing(self) -> bool:
        return self.placing

    @classmethod
    def getDataFrom(cls, type: str) -> dict:
        return cls.BUILDINGS_DATA[type]
