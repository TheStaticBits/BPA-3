import logging
import random
from src.utility.image import Image
from src.utility.vector import Vect
from src.window import Window
from src.utility.timer import Timer


class Particle:
    """ Used for enemy death particle effects and perhaps other things """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the particle animation data from consts """
        cls.ANIMS: dict = constants["particles"]

    def __init__(self, parentImg: Image, size: Vect,
                 pos: Vect, angle: float,
                 speed: float, duration: float) -> None:
        """ Initialize particle with a random section from the given image """

        # Random position within the parent image for the particle to use
        randPos: Vect = Vect(
            random.randint(0, parentImg.getSize().x - size.x),
            random.randint(0, parentImg.getSize().y - size.y)
        )

        # Create the particle image from the parent image
        self.image: Image = parentImg.getSection(randPos, size)

        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.timer = Timer(duration)

        self.opacity = 255

    def update(self, window: Window) -> None:
        """ Moves the particle along and fades it out """
        self.timer.update(window)
        self.opacity = int(255 * (1 - self.timer.getPercentDone()))

        moveAmount: Vect = Vect.angleMove(self.angle) * \
            self.speed * window.getDeltaTime()

        self.pos += moveAmount

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the particle at the current opacity """
        self.image.setAlpha(self.opacity)
        surface.render(self.image, self.pos + offset)

    def isDone(self) -> bool:
        """ Returns True if the particle has finished """
        return self.timer.isDone()
