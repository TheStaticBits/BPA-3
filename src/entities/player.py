from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect


class Player(Entity):
    """ Inherits from Entity class.
        Handles player functionality and movement """

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Load static variables from constants dict """
        cls.ANIM: dict = constants["player"]["anim"]

        cls.MAX_SPEED: float = constants["player"]["maxSpeed"]
        cls.ACCELERATION: float = constants["player"]["acceleration"]
        cls.DECELERATION: float = constants["player"]["deceleration"]

        # Player resources
        cls.resources: dict = constants["player"]["resources"]

    def __init__(self, startingPos: Vect) -> None:
        """ Initialize player objects and data """
        super().__init__(self.ANIM, __name__, pos=startingPos)

        self.log.info("Initializing player")

        self.velocity = Vect(0, 0)

    def update(self, window: Window, entities: list[Entity] = None) -> None:
        """ Update player animation, movement, etc. """
        super().update(window)

        self.movement(window)

        # Move player based on velocity while checking collisions
        super().collision(window, entities, self.velocity)

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
        self.velocity.forEach(decelerate, vectParams=[acceleration])

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (super().getCenterPos() / tileSize).floor()

    @classmethod
    def getResource(cls, resource: str) -> int:
        return cls.resources[resource]

    @classmethod
    def getAllResources(cls) -> None:
        return cls.resources

    # Setters
    @classmethod
    def addResource(cls, resource: str, amount: int) -> None:
        cls.resources[resource] += amount
