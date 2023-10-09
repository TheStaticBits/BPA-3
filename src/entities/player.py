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

        self.MAX_SPEED = constants["player"]["maxSpeed"]
        self.ACCELERATION = constants["player"]["acceleration"]
        self.DECELERATION = constants["player"]["deceleration"]

        self.velocity = Vect(0, 0)
    

    def update(self, window: Window) -> None:
        """ Update player animation, movement, etc. """
        super().update(window)

        self.movement(window)

    
    def movement(self, window: Window) -> None:
        """ Handle player movement based on inputs """

        # Gets movement direction based on the keys pressed (getKey is 1 or 0)
        acceleration: Vect = Vect(window.getKey("right") - window.getKey("left"), 
                                  window.getKey("down") - window.getKey("up"))

        self.velocity += acceleration * self.ACCELERATION * window.getDeltaTime()
        
        # Lock between the max an min speed
        self.velocity.clamp(Vect(-self.MAX_SPEED), Vect(self.MAX_SPEED))

        # Deceleration when the player is not inputting
        # and the velocity is not 0
        if acceleration.x == 0 and self.velocity.x != 0:
            self.velocity.x -= (-1 if self.velocity.x < 0 else 1) * self.DECELERATION * window.getDeltaTime()
        if acceleration.y == 0 and self.velocity.y != 0:
            self.velocity.y -= (-1 if self.velocity.y < 0 else 1) * self.DECELERATION * window.getDeltaTime()

        super().addPos(self.velocity * window.getDeltaTime())
    

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (self.getCenterPos() / tileSize).floor()