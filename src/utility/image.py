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
        try:
            cls.SCALE = constants["game"]["imgScale"]
        except KeyError:
            # avoid circular import
            from src.ui.interfaces.errorUI import ErrorUI
            ErrorUI.create(
                "Missing game -> imgScale in constants. Defaulting to 3",
                cls.log, recoverable=True
            )
            cls.SCALE = 3

    @staticmethod
    def makeEmpty(size: Vect, scale=False, transparent=False) -> Image:
        """ Creates an empty transparent surface with a given size """
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if transparent:
            flags |= pygame.SRCALPHA

        surf = pygame.Surface(size.toTuple(), flags)

        return Image(surf=surf, scale=scale)

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

    def render(self, other: Image, pos: Vect = Vect(),
               area: pygame.Rect = None) -> None:
        """ Renders another image to this image at a given pos """
        self.image.blit(other.image, pos.toTuple(), area=area)

    def fill(self, *color) -> None:
        """ Fills the image with a given color """
        self.image.fill(color)

    def tint(self, *color, blendMode=pygame.BLEND_MULT) -> None:
        """ Tints the image with a given color """
        self.image.fill(color, special_flags=blendMode)

    def copy(self) -> Image:
        """ Returns a copy of the image """
        return Image(surf=self.image.copy(), scale=False)

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

    def drawCircle(self, radius: int, color: tuple[int, int, int]) -> None:
        """ Draws a circle centered on the image """
        pygame.draw.circle(self.image, color,
                           (self.size // 2).toTuple(), radius)

    def pixelPerfectCollide(self, thisPos: Vect,
                            other: Image, otherPos: Vect) -> bool:
        """ Returns whether the two images collide """
        offset: Vect = otherPos - thisPos

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(other.image)

        return mask1.overlap(mask2, offset.toTuple())

    def getSection(self, pos: Vect, size: Vect) -> Image:
        """ Returns a subsurface of the image """
        rect = pygame.Rect(pos.toTuple(), size.toTuple())  # Create rect
        subsurface = self.image.subsurface(rect)  # Get pygame.Surface subsurf
        return Image(surf=subsurface, scale=False)  # Return as Image

    # Getters
    def getSurf(self) -> pygame.Surface: return self.image
    def getSize(self) -> Vect: return self.size
    def getWidth(self) -> int: return self.size.x
    def getHeight(self) -> int: return self.size.y
