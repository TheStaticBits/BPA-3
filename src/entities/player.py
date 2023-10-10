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

        self.MAX_SPEED: float = constants["player"]["maxSpeed"]
        self.ACCELERATION: float = constants["player"]["acceleration"]
        self.DECELERATION: float = constants["player"]["deceleration"]

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


        # Decelerate velocity if the player is not inputting movement
        # Used for each axis on the velocity Vect separately
        def decelerate(velocity: float, acceleration: float) -> float:
            """ Returns the decelerated value for the given velocity """
            if acceleration == 0: # player is not inputting movement in this direction
                # get direction of velocity (positive or negative):
                if velocity < 0: dir: int = -1
                else: dir: int = 1

                # decelerate towards zero
                velocity -= dir * self.DECELERATION * window.getDeltaTime()
                
                # if the velocity has passed zero, set it to zero,
                # useful for low framerates
                if velocity * dir < 0:
                    velocity = 0
            
            return velocity


        # Apply the above decelerate function for each axis
        self.velocity.forEach(decelerate,
                              paramsX=[acceleration.x],
                              paramsY=[acceleration.y])

        super().addPos(self.velocity * window.getDeltaTime())
    

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (self.getCenterPos() / tileSize).floor()