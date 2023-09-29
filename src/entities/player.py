import pygame, logging

from src.entities.entity import Entity
from src.window import Window

class Player(Entity):
    """ Inherits from Entity class. 
        Handles player functionality and movement """
    
    def __init__(self, constants: dict) -> None:
        """ Initialize player objects and data """
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing player")

        super().__init__(constants["player"]["anim"])
    

    def update(self, window: Window) -> None:
        super().update(window)