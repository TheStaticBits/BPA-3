import pygame, logging

from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect

class Player(Entity):
    """ Inherits from Entity class. 
        Handles player functionality and movement """
    
    def __init__(self, constants: dict, startingPos: Vect) -> None:
        """ Initialize player objects and data """
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing player")

        super().__init__(constants["player"]["anim"], pos=startingPos)

        self.SPEED = constants["player"]["speed"]
    

    def update(self, window: Window) -> None:
        """ Update player animation, movement, etc. """
        super().update(window)

        self.movement(window)

    
    def movement(self, window: Window) -> None:
        """ Handle player movement based on inputs """

        # Gets movement direction based on the keys pressed (getKey is 1 or 0)
        move: Vect = Vect(window.getKey("right") - window.getKey("left"), 
                          window.getKey("down") - window.getKey("up"))
        
        # Amount moved in pixels based on the direction and speed
        movePixels = move * self.SPEED * window.getDeltaTime()

        super().addPos(movePixels)
    

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (self.getCenterPos() / tileSize).floor()