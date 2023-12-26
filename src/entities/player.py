import logging
from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect
from src.utility.advDict import AdvDict
from src.utility.image import Image
from src.tileset import Tileset
from src.ui.interfaces.errorUI import ErrorUI


class Player(Entity):
    """ Inherits from Entity class.
        Handles player functionality and movement """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Load static variables from constants dict """
        cls.ANIM: dict = constants["player"]["anim"]

        try:
            cls.MAX_SPEED: float = constants["player"]["maxSpeed"] * \
                Image.SCALE
        except KeyError:
            ErrorUI.create("Unable to find player: maxSpeed in constants.json",
                           cls.log, recoverable=True)
            cls.MAX_SPEED: float = 100 * Image.SCALE

        cls.ACCELERATION: float = constants["player"]["accel"] * Image.SCALE
        cls.DECELERATION: float = constants["player"]["decel"] * Image.SCALE

        # Player resources
        cls.resources = AdvDict(constants["player"]["resources"]["starting"])
        cls.resLimits = AdvDict(constants["player"]["resources"]["limits"])
        cls.resLabels = AdvDict(constants["player"]["resources"]["labels"])

    @classmethod
    def capResources(cls) -> None:
        """ If any resources are above their limit, set them to the limit """
        for resource in cls.resources.getPyDict().keys():
            if cls.resLimits[resource] < 0:
                continue

            if cls.resources[resource] > cls.resLimits[resource]:
                cls.resources[resource] = cls.resLimits[resource]

    def __init__(self, startingPos: Vect) -> None:
        """ Initialize player objects and data """
        super().__init__(self.ANIM, pos=startingPos)

        self.log.info("Initializing player")

        self.velocity = Vect(0, 0)

    def update(self, window: Window, tileset: Tileset,
               buildings: list[Entity] = []) -> None:
        """ Update player animation, movement, etc. """
        super().update(window)

        self.movement(window)

        # Remove buildings that are being placed:
        buildings = [b for b in buildings if not b.isPlacing()]

        # Move player based on velocity while checking collisions
        super().collision(window, buildings, self.velocity)

        # Prevent player from walking out of the map boundaries
        super().lockToRect(Vect(0, 0), tileset.getSize(), self.velocity)

    def movement(self, window: Window) -> None:
        """ Handle player movement based on inputs """

        # Gets movement direction based on the keys pressed (getKey is 1 or 0)
        acceleration = Vect(window.getKey("right") - window.getKey("left"),
                            window.getKey("down") - window.getKey("up"))

        self.velocity += (acceleration *
                          self.ACCELERATION *
                          window.getDeltaTime())

        # Lock between the max an min speed
        self.velocity.clamp(Vect(-self.MAX_SPEED), Vect(self.MAX_SPEED))

        # Decelerate velocity if the player is not inputting movement
        # Used for each axis on the velocity Vect separately
        def decelerate(velocity: float, acceleration: float) -> float:
            """ Returns the decelerated value for the given velocity """

            # Test if player is not inputting movement in this direction
            if acceleration == 0:
                # get direction of velocity (positive or negative):
                if velocity < 0:
                    dir: int = -1
                else:
                    dir: int = 1

                # decelerate towards zero
                velocity -= dir * self.DECELERATION * window.getDeltaTime()

                # if the velocity has passed zero, set it to zero,
                # useful for low framerates
                if velocity * dir < 0:
                    velocity = 0

            return velocity

        # Apply the above decelerate function for each axis,
        # with acceleration as the parameter of the decelerate function
        self.velocity = self.velocity.forEach(decelerate,
                                              vectParams=[acceleration])

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (super().getCenterPos() / tileSize).floor()
