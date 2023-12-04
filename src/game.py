import logging

import src.utility.utility as util
from src.utility.image import Image
from src.window import Window
from src.tileset import Tileset
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.player import Player
from src.entities.warrior import Warrior
from src.scenes.baseScene import BaseScene
from src.scenes.sceneManager import SceneManager
from src.ui.elements.text import Text
from src.ui.interfaces.baseUI import BaseUI


class Game:
    def __init__(self, CONSTANTS_FILE: str) -> None:
        """ Initialize game objects and data"""

        # Setup constants and logger
        self.constants: dict = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        self.log = logging.getLogger(__name__)
        self.log.info("Initializing game")

        self.loadStatic()

        # Window
        self.window: Window = Window()

        # Scene manager
        self.sceneManager: SceneManager = SceneManager()

    def loadStatic(self) -> None:
        """ Loading static data from the constants JSON file """
        Image.loadStatic(self.constants)
        Window.loadStatic(self.constants)
        Tileset.loadStatic(self.constants)
        BaseBuilding.loadStatic(self.constants)
        Player.loadStatic(self.constants)
        Warrior.loadStatic(self.constants)
        BaseScene.loadStatic(self.constants)
        BaseUI.loadStatic(self.constants)
        Text.loadStatic(self.constants)

    def mainLoop(self) -> None:
        while not self.window.isClosed():
            self.window.handleInputs()

            # Update functions
            self.sceneManager.update(self.window)

            # Render functions
            self.sceneManager.render(self.window)

            self.window.update()
