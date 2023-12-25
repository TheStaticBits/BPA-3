from __future__ import annotations
import pygame
import logging

from src.utility.vector import Vect


class Image:
    """ Contains a single pygame.Surface object for images
        Reduces loading the same image multiple times,
        and contains easy functions for rendering and others """
    log = logging.getLogger(__name__)

    # Static variable for all images to avoid duplicates
    # Key: path, value: pygame.Surface (the image)
    images: dict[str, pygame.Surface] = {}

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        cls.SCALE = constants["game"]["imgScale"]

    def __init__(self, path: str = None,
                 surf: pygame.Surface = None,
                 scale: bool = True) -> None:
        """ Loads and scales up (if necessary) an image
            from a given filepath, or use a given Pygame surface """
        if path is None and surf is None:
            raise ValueError("Either path or surf must be given")

        self.image = surf

        if path is not None:
            # Load image if it hasn't been loaded before
            if path not in self.images:
                self.images[path] = pygame.image.load(path).convert_alpha()
                self.log.info(f"Loaded image {path}")

            self.image = self.images[path]

        # Get size of image
        self.size: Vect = Vect(self.image.get_size())

        if scale and self.SCALE != 1:
            # Scale image up by the scale factor
            self.transform(self.size * self.SCALE)

    def render(self, other: Image, pos: Vect,
               area: pygame.Rect = None) -> None:
        """ Renders another image to this image at a given pos """
        self.image.blit(other.image, pos.toTuple(), area=area)

    def fill(self, *color) -> None:
        """ Fills the image with a given color """
        self.image.fill(color)

    def setAlpha(self, alpha: int) -> None:
        """ Sets the alpha of the image """
        self.image.set_alpha(alpha)

    def transform(self, size: Vect) -> None:
        """ Transforms the image to the given size """
        self.image = pygame.transform.scale(self.image, size.toTuple())
        self.size = size

    def rotate(self, degrees: float) -> None:
        """ Rotates the image by the given degrees """
        if degrees != 0:
            self.image = pygame.transform.rotate(self.image, degrees)

    def flip(self, x: bool, y: bool) -> None:
        """ Flips the image on the x and/or y axis """
        self.image = pygame.transform.flip(self.image, x, y)

    # Getters
    def getSurf(self) -> pygame.Surface: return self.image
    def getSize(self) -> Vect: return self.size
    def getWidth(self): return self.size.x
    def getHeight(self): return self.size.y
