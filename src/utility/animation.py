import pygame
import logging

from src.window import Window
from src.utility.vector import Vect
from src.utility.image import Image
from src.utility.timer import Timer


class Animation:
    """ Class for handling animations,
        including updating and rendering.
        Only works with horizontal spritesheets """
    log = logging.getLogger(__name__)

    def __init__(self, path: str, frameCount: int, delay: float,
                 oneTime: bool = False) -> None:
        """ Sets initial values for the animation """
        self.spritesheet: Image = Image(path)
        self.timer = Timer(delay)

        if self.spritesheet.getWidth() % frameCount != 0:
            self.log.error("Spritesheet width is not divisible by frame count")

        self.frameSize = Vect(self.spritesheet.getWidth() / frameCount,
                              self.spritesheet.getHeight())

        self.frameCount = frameCount
        self.currentFrame: int = 0

        self.oneTime: bool = oneTime

    def update(self, window: Window) -> None:
        """ Updates animation timer and frame if necessary """
        if self.oneTime and self.currentFrame >= self.frameCount:
            return  # Don't update if the animation is one time and completed

        self.timer.update(window)

        # while the timer is completed (so it works on low FPS):
        while self.timer.completed():
            self.currentFrame += 1

            # Reached the end of the animation
            if self.currentFrame >= self.frameCount:
                if self.oneTime:  # One time, so don't reset current frame
                    self.timer.reset()
                else:
                    self.currentFrame = 0  # Continue looping

    def render(self, surface: Window | Image, pos: Vect) -> None:
        """ Renders the portion of the animation spritesheet
            that's the current frame to the window """

        # Gets the coordinates and size of the current frame of the spritesheet
        area = pygame.Rect(self.currentFrame * self.frameSize.x, 0,
                           self.frameSize.x, self.frameSize.y)

        surface.render(self.spritesheet, pos, area=area)

    # Getters
    def getSize(self) -> Vect: return self.frameSize

    def getFrame(self, frame: int = None) -> Image:
        """ Returns the given frame of the spritesheet """
        if frame is None:
            frame = self.currentFrame

        # Position of the frame on the spritesheet
        pos: Vect = Vect(frame * self.frameSize.x, 0)

        # Get new image of only the frame
        return self.spritesheet.getSection(pos, self.frameSize)

    def isFinished(self) -> bool: return self.currentFrame >= self.frameCount

    # Setters
    def restart(self) -> None: self.currentFrame = 0
    def setToEnd(self) -> None: self.currentFrame = self.frameCount
