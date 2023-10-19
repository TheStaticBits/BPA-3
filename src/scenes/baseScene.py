import logging

from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.window import Window


class BaseScene:
    """ Handles/contains tileset, player, camera offset,
        and other scene-related things """

    CAMERA_SPEED: float = None

    @classmethod
    def loadStatic(cls, constants: str):
        cls.CAMERA_SPEED = constants["game"]["cameraSpeed"]

    def __init__(self, constants: dict, mapFolderName: str,
                 loggerName: str) -> None:
        """ Sets up logger, tileset, players, and camera offset """

        self.log = logging.getLogger(loggerName)

        self.log.info("Initializing scene for map " + mapFolderName)

        self.tileset: Tileset = Tileset(mapFolderName)
        self.player: Player = Player(constants, self.tileset.getPlayerStart())

        self.cameraOffset: Vect = Vect()

    def update(self, window: Window) -> None:
        """ Update scene objects """
        self.tileset.update(window)

        self.player.update(window)

        self.updateCameraPos(window)

    def updateCameraPos(self, window: Window) -> None:
        """ Update camera position """
        # Camera position centered on the position
        newOffset = self.player.getCenterPos() - window.getWindowSize() / 2

        # Move the camera offset slowly to the new position
        self.cameraOffset += ((newOffset - self.cameraOffset) *
                              self.CAMERA_SPEED * window.getDeltaTime())

    def render(self, window: Window) -> None:
        """ Render scene objects """
        self.renderTileset(window)
        self.renderPlayer(window)

    def renderTileset(self, window: Window) -> None:
        """ Render the tileset """
        self.tileset.render(window, -self.cameraOffset)

    def renderPlayer(self, window: Window) -> None:
        """ Render the player """
        self.player.render(window, -self.cameraOffset)

    # Getters
    def getCamOffset(self) -> Vect: return self.cameraOffset
    def getPlayer(self) -> Player: return self.player
    def getTileset(self) -> Tileset: return self.tileset
