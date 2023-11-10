import logging

from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window
from src.ui.interfaces.resourcesUI import ResourcesUI


class BaseScene:
    """ Handles/contains tileset, player, camera offset,
        and other scene-related things """

    @classmethod
    def loadStatic(cls, constants: str):
        cls.CAMERA_SPEED: float = constants["game"]["cameraSpeed"]

    def __init__(self, mapFolderName: str, loggerName: str) -> None:
        """ Sets up logger, tileset, players, and camera offset """

        self.log = logging.getLogger(loggerName)

        self.log.info("Initializing scene for map " + mapFolderName)

        self.tileset: Tileset = Tileset(mapFolderName)
        self.player: Player = Player(self.tileset.getPlayerStart())

        self.cameraOffset: Vect = Vect()

        # Handling resource numbers and icons in the top left
        self.resourcesUI = ResourcesUI()

    def update(self, window: Window) -> None:
        """ Update scene objects """
        self.updateCameraPos(window)

        self.updateTileset(window)
        self.updatePlayer(window)
        self.updateUI(window)

    def updateTileset(self, window: Window) -> None:
        """ Update tileset """
        self.tileset.update(window)

    def updatePlayer(self, window: Window) -> None:
        """ Update player """
        self.player.update(window)

    def updateUI(self, window: Window) -> None:
        """ Update any universal scene UIs """
        self.resourcesUI.update(window)

    def updateCameraPos(self, window: Window) -> None:
        """ Update camera position """
        # Camera position centered on the position
        newOffset = self.player.getCenterPos() - window.getSize() / 2

        # Clamp between 0, 0 and max camera offset
        newOffset.clamp(
            Vect(),  # 0, 0
            self.tileset.getSize() - window.getSize()
        )

        # Move the camera offset slowly to the new position
        self.cameraOffset += ((newOffset - self.cameraOffset) *
                              self.CAMERA_SPEED * window.getDeltaTime())

    def render(self, surface: Window | Image) -> None:
        """ Render scene objects """
        self.renderTileset(surface)
        self.renderPlayer(surface)

    def renderTileset(self, surface: Window | Image) -> None:
        """ Render the tileset """
        self.tileset.render(surface, -self.cameraOffset)

    def renderPlayer(self, surface: Window | Image) -> None:
        """ Render the player """
        self.player.render(surface, -self.cameraOffset)

    def renderUI(self, surface: Window | Image) -> None:
        """ Render any universal scene UIs """
        self.resourcesUI.render(surface)

    # Getters
    def getCamOffset(self) -> Vect: return self.cameraOffset
    def getPlayer(self) -> Player: return self.player
    def getTileset(self) -> Tileset: return self.tileset
