import pygame

import src.utility.utility as util
from src.window import Window

class Game:
    def __init__(self, CONSTANTS_FILE):
        """ Initialize game objects and data"""
        
        # Setup constants and logger
        self.constants = util.loadJSON(CONSTANTS_FILE)
        util.setupLogger(self.constants)

        # Window
        self.window = Window()

    def mainLoop(self):
        pass