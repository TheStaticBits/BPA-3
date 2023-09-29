import pygame, logging

import src.utility.utility as util
from src.window import Window
from src.entities.player import Player

class Game:
    def __init__(self, CONSTANTS_FILE: str) -> None:
        """ Initialize game objects and data"""
        
        # Setup constants and logger
        self.constants: dict = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        self.log = logging.getLogger(__name__)
        self.log.info("Initializing game")

        # Get image scale
        util.IMG_SCALE = self.constants["window"]["imgScale"]

        # Window
        self.window: Window = Window(self.constants)

        # player (testing)
        self.player: Player = Player(self.constants)


    def mainLoop(self) -> None:
        while not self.window.isClosed():
            self.window.handleInputs()

            self.player.update(self.window)
            self.player.render(self.window)

            self.window.update()