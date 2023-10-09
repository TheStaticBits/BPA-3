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

        self.velocity = Vect(0, 0)
    

    def update(self, window: Window) -> None:
        """ Update player animation, movement, etc. """
        super().update(window)

        self.movement(window)

    
    def movement(self, window: Window) -> None:
        """ Handle player movement based on inputs """

        acceleration: Vect = Vect(window.getKey("right") - window.getKey("left"), 
                             window.getKey("down") - window.getKey("up"))

        # Gets movement direction based on the keys pressed (getKey is 1 or 0)

        self.velocity += acceleration #* window.getDeltaTime()

        if -200 > self.velocity.x or self.velocity.x > 200:
            self.velocity.x = 200 * (self.velocity.x/abs(self.velocity.x))
        if -200 > self.velocity.y or self.velocity.y > 200:
            self.velocity.y = 200 * (self.velocity.y/abs(self.velocity.y))
        

        if(acceleration.x == 0 and self.velocity.x != 0):
            self.velocity.x += ((self.velocity.x/abs(self.velocity.x))* -2)
        if acceleration.y == 0 and self.velocity.y != 0:
            self.velocity.y += ((self.velocity.y/abs(self.velocity.y))* -2)
        

        
        # Amount moved in pixels based on the direction and speed
        movePixels = self.velocity * self.SPEED * 1/80 * window.getDeltaTime()

        super().addPos(movePixels)
    

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (self.getCenterPos() / tileSize).floor()