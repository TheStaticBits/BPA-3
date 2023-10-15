import logging

import src.utility.utility as util
from src.window import Window
from src.tileset import Tileset
from src.entities.building import Building
from src.entities.warrior import Warrior
from src.scenes.baseScene import BaseScene
from src.scenes.buildingsScene import BuildingsScene
from src.ui.elements.text import Text
from src.ui.baseUI import BaseUI


class Game:
    def __init__(self, CONSTANTS_FILE: str) -> None:
        """ Initialize game objects and data"""

        # Setup constants and logger
        self.constants: dict = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        self.log = logging.getLogger(__name__)
        self.log.info("Initializing game")

        # Get image scale
        util.IMG_SCALE = self.constants["game"]["imgScale"]

        # Loading static data from the constants JSON file
        Tileset.loadStatic(self.constants)
        Building.loadStatic(self.constants)
        Warrior.loadStatic(self.constants)
        BaseScene.loadStatic(self.constants)
        BaseUI.loadStatic(self.constants)
        Text.loadStatic(self.constants)

        # Window
        self.window: Window = Window(self.constants)

        # Test scene
        self.buildingsScene: BuildingsScene = BuildingsScene(self.constants,
                                                             "testmap")

    def mainLoop(self) -> None:
        while not self.window.isClosed():
            self.window.handleInputs()

            # Update functions
            self.buildingsScene.update(self.window)

            # Render functions
            self.buildingsScene.render(self.window)

            self.window.update()
