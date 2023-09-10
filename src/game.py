import pygame, logging

import src.utility.utility as util
from src.window import Window

class Game:
    def __init__(self, CONSTANTS_FILE):
        """ Initialize game objects and data"""
        
        # Setup constants and logger
        self.constants = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        self.log = logging.getLogger(__name__)

        self.log.info("Initializing game")

        # Window
        self.window = Window(self.constants)


    def mainLoop(self):
        while not self.window.isClosed():
            self.window.handleInputs()

            # Game logic here

            self.window.update()