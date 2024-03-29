import logging
from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect
from src.utility.advDict import AdvDict
from src.utility.image import Image
from src.tileset import Tileset
from src.ui.interfaces.errorUI import ErrorUI
from src.utility.animation import Animation


class Player(Entity):
    """ Inherits from Entity class.
        Handles player functionality and movement """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Load static variables from constants dict """
        try:
            cls.ANIMS: dict = constants["player"]["anims"]
        except KeyError:
            ErrorUI.create("Unable to find player -> anims in constants",
                           cls.log)

        # Max velocity/speed
        try:
            cls.MAX_SPEED: float = constants["player"]["maxSpeed"] * \
                Image.SCALE
        except KeyError:
            ErrorUI.create("Unable to find player -> maxSpeed in constants",
                           cls.log, recoverable=True)
            cls.MAX_SPEED: float = 100 * Image.SCALE

        # Acceleration, decceleration
        try:
            cls.ACCELERATION: float = constants["player"]["accel"] * \
                Image.SCALE
            cls.DECELERATION: float = constants["player"]["decel"] * \
                Image.SCALE
        except KeyError:
            ErrorUI.create("Unable to find player -> [accel or decel] "
                           "in constants.json. Using default values.",
                           cls.log, recoverable=True)
            cls.ACCELERATION: float = 400 * Image.SCALE
            cls.DECELERATION: float = 550 * Image.SCALE

        try:
            # Player starting resources
            cls.STARTNG_RES = AdvDict(
                constants["player"]["resources"]["start"]
            )
            # resource limits (max amounts), -1 means no limit
            cls.RES_LIMITS = AdvDict(
                constants["player"]["resources"]["limits"]
            )
            # display names for resources
            cls.RES_LABELS = AdvDict(
                constants["player"]["resources"]["labels"]
            )

            cls.resetResources()
        except KeyError:
            ErrorUI.create("Unable to find player -> resources -> "
                           "[start, limits, or labels] data in constants",
                           cls.log)

        try:
            # Distance that the player needs to be to hear a sound
            cls.HEARING_RANGE: float = constants["player"]["hearingRange"] * \
                Image.SCALE
        except KeyError:
            ErrorUI.create("Unable to find player -> hearingRange"
                           " in constants. Defaulting to 100",
                           cls.log, recoverable=True)
            cls.HEARING_RANGE: float = 100 * Image.SCALE

    @classmethod
    def capResources(cls) -> None:
        """ If any resources are above their limit, set them to the limit """
        for resource in cls.resources.getPyDict().keys():
            if cls.resLimits[resource] < 0:
                continue

            if cls.resources[resource] > cls.resLimits[resource]:
                cls.resources[resource] = cls.resLimits[resource]

    @classmethod
    def resetResources(cls) -> None:
        """ Reset resources to starting resources """
        cls.resources = cls.STARTNG_RES.copy()
        cls.resLimits = cls.RES_LIMITS.copy()

    def __init__(self, startingPos: Vect) -> None:
        """ Initialize player objects and data """
        super().__init__(pos=startingPos)

        self.animations: dict[Animation] = {
            "idle": super().loadAnim(self.ANIMS["idle"]),
            "walking": super().loadAnim(self.ANIMS["walking"]),
        }

        self.currentAnim = None
        self.setAnimation("idle")

        self.log.info("Initializing player")

        self.velocity = Vect(0, 0)

    def update(self, window: Window, tileset: Tileset,
               buildings: list[Entity] = []) -> Entity | None:
        """ Update player animation, movement, etc.
            Returns the first building the player has collided with """
        super().update(window)

        self.movement(window)
        self.updateMovementAnim()

        # Remove buildings that are being placed:
        buildings = [b for b in buildings if not b.isPlacing()]

        # Move player based on velocity while checking collisions
        collided = super().collision(window, buildings, self.velocity)

        # Prevent player from walking out of the map boundaries
        super().lockToRect(Vect(0, 0), tileset.getSize(), self.velocity)

        # Return the first collided building if the list isn't empty
        return collided[0] if len(collided) != 0 else None

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

    def updateMovementAnim(self) -> None:
        """ Changes animation based on player velocity """
        # Set animation based on if the player is moving or not
        moving: bool = self.velocity != Vect()
        animation = "idle" if not moving else "walking"
        self.setAnimation(animation)

    def setAnimation(self, anim: str) -> None:
        """ Sets the animation to the given animation name """
        if anim == self.currentAnim:
            return

        self.currentAnim = anim
        self.animations[anim].restart()
        super().setAnim(self.animations[anim])

    def getSoundVolume(self, pos: Vect) -> None:
        """ Returns the volume of a sound given its position """
        dist: float = pos.dist(super().getCenterPos())

        if dist > self.HEARING_RANGE:
            return 0

        return 1 - (dist / self.HEARING_RANGE)

    # Getters
    def getTilePos(self, tileSize: Vect) -> Vect:
        """ Returns the player's position in tiles """
        return (super().getCenterPos() / tileSize).floor()
