import logging

from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.window import Window

class Scene:
    """ Contains tileset, player, buildings, etc.
        Manages camera offset and other scene-related things """
    
    def __init__(self, constants: dict, mapFolderName: str) -> None:
        self.log = logging.getLogger(__name__)

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
        self.cameraOffset = self.findCameraPos(window)
    

    def render(self, window: Window) -> None:
        """ Render scene objects """
        self.tileset.render(window, self.cameraOffset * -1)
        self.player.render(window, self.cameraOffset * -1)
    

    def findCameraPos(self, window: Window) -> Vect:
        """ Returns the camera position """
        # Finding the camera position centered on the player
        return self.player.getPos() + (self.player.getAnim().getSize() / 2) - window.getWindowSize() / 2