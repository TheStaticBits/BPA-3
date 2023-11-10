from __future__ import annotations
import pygame

from src.utility.vector import Vect


class Image:
    """ Contains a single pygame.Surface object for images
        Reduces loading the same image multiple times,
        and contains easy functions for rendering and others """

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

    def transform(self, size: Vect) -> None:
        """ Transforms the image to the given size """
        self.image = pygame.transform.scale(self.image, size.toTuple())
        self.size = size

    # Getters
    def getSurf(self) -> pygame.Surface: return self.image
    def getSize(self) -> Vect: return self.size
    def getWidth(self): return self.size.x
    def getHeight(self): return self.size.y
