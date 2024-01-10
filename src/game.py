import logging

import src.utility.utility as util
from src.utility.image import Image
from src.window import Window
from src.tileset import Tileset
from src.waves import Waves
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.player import Player
from src.entities.warrior import Warrior
from src.entities.projectile import Projectile
from src.scenes.baseScene import BaseScene
from src.sceneManager import SceneManager
from src.ui.elements.text import Text
from src.ui.interfaces.baseUI import BaseUI
from src.ui.interfaces.errorUI import ErrorUI
from src.utility.database import Database


class Game:
    log = logging.getLogger(__name__)

    def __init__(self, CONSTANTS_FILE: str) -> None:
        """ Initialize game objects and data """

        # Load constants and setup logger
        self.constants: dict = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        self.log.info("Initializing game")

        # Create database
        self.database: Database = Database(self.constants["saves"]["saveFile"])

        # Load static data from the constants JSON file
        self.loadStatic()

        # Create objects
        self.window: Window = Window()
        self.errorUI: ErrorUI = ErrorUI()
        self.sceneManager: SceneManager = SceneManager(self.window,
                                                       self.database)

    def loadStatic(self) -> None:
        """ Loading static data from the constants JSON file """
        self.log.info("Loading static data from constants.json")

        try:
            Image.loadStatic(self.constants)
            BaseUI.loadStatic(self.constants)
            Text.loadStatic(self.constants)
            ErrorUI.loadStatic(self.constants)

            Window.loadStatic(self.constants)
            Tileset.loadStatic(self.constants)
            BaseBuilding.loadStatic(self.constants)
            Warrior.loadStatic(self.constants)
            Projectile.loadStatic(self.constants)
            BaseScene.loadStatic(self.constants)
            Player.loadStatic(self.constants)
            Waves.loadStatic(self.constants)

        except KeyError:
            ErrorUI.create("Uncaught error loading data from JSON files",
                           self.log)

    def mainLoop(self) -> None:
        """ Main game loop, call to start game """
        # Main game loop until window is closed
        while not self.window.isClosed():
            self.window.handleInputs()
            self.errorUI.update(self.window)

            # Run the frame, catching any errors in the game
            try:
                self.iteration()
            except Exception:
                ErrorUI.create("Uncaught error in game loop", self.log)

            self.errorUI.render(self.window)
            self.window.update()

    def iteration(self) -> None:
        """ Each iteration of the game loop """

        # Allow rendering of the game if there is a recoverable error
        if self.errorUI.isHidden() or ErrorUI.isRecoverable():
            self.update()
            self.render()

    def update(self) -> None:
        """ Each update iteration of the game loop """
        self.sceneManager.update(self.window)

    def render(self) -> None:
        """ Each render iteration of the game loop """
        self.sceneManager.render(self.window)

    def save(self) -> None:
        """ Saves the game data """

        self.database.saveAndClose()
