from __future__ import annotations
import logging
import random
import math
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

    def __init__(self, parentImg: Image, pos: Vect, size: Vect,
                 speed: float, duration: float) -> None:
        """ Initialize particle with a random section from the given image """

        parentSize: Vect = parentImg.getSize()

        # Random position within the parent image for the particle to use
        randPos: Vect = Vect(
            random.randint(0, parentSize.x - size.x),
            random.randint(0, parentSize.y - size.y)
        )

        # Create the particle image from the parent image
        self.image: Image = parentImg.getSection(randPos, size)

        self.pos = pos + randPos
        self.timer = Timer(duration)
        self.speed = speed

        centerPos = parentSize / 2
        if centerPos == randPos:
            # Random angle if the random pos was in the center
            self.angle = math.radians(random.randint(0, 359))
        else:
            # Angle from randPos to the center of the image
            self.angle = centerPos.angle(randPos)

        self.opacity = 255

    def update(self, window: Window) -> None:
        """ Moves the particle along and fades it out """
        self.timer.update(window)

        # Opacity and speed die down based on how much time is left
        percentLeft: float = 1 - self.timer.getPercentDone()
        self.opacity = int(255 * percentLeft)
        speed = self.speed * percentLeft

        # Movement of the particle
        moveAmount: Vect = Vect.angleMove(self.angle) * \
            speed * window.getDeltaTime()

        self.pos += moveAmount

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the particle at the current opacity """
        self.image.setAlpha(self.opacity)
        surface.render(self.image, self.pos + offset)

    def isDone(self) -> bool:
        """ Returns True if the particle has finished """
        return self.timer.isDone()

    @staticmethod
    def generate(amount: int, parentImg: Image, pos: Vect, size: Vect,
                 speed: float, duration: float) -> list[Particle]:
        """ Generates a list of particles """
        particles: list = []

        for _ in range(amount):
            particles.append(Particle(parentImg, pos, size, speed, duration))

        return particles
