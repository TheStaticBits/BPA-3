import pygame
import logging

class Window:
    def __init__(self):
        self.log = logging.getLogger(__name__)

        self.log.info("e")
        self.log.warning("Initializing window...")
        self.log.error("Failed window...")