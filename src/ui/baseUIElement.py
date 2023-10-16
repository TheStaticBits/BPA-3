import pygame
import logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.window import Window


class BaseUIElement:
    """ All UI elements (text, buttons, etc.) inherit
        from this class, which handles image loading,
        storage, and rendering """

    # Static, stores all loaded images to prevent duplicates
    # Key: string (the image's path)
    # Value: pygame.Surface (the image)
    images: dict = {}

    def __init__(self, data: dict, loggerName: str,
                 imgPath: str = None) -> None:

        self.log = logging.getLogger(loggerName)

        # Offset from top left corner of each UI
        self.offset: Vect = Vect(data["offset"])

        self.centered: bool = data["centered"] if "centered" in data else False

        self.image: pygame.Surface = None
        self.size: Vect = None
        self.renderPos: Vect = None

        if imgPath is not None:
            self.setImg(self.loadImg(imgPath))

    def loadImg(self, imgPath: str) -> pygame.Surface:
        """ Loads an image from the given path if it has
            not been loaded already, and returns it """
        if imgPath not in self.images:
            self.images[imgPath] = util.loadImg(imgPath)  # loads and stores

        return self.images[imgPath]

    def update(self, window: Window, offset: Vect) -> None:
        """ Calculates renderPos based on offset and UI offset,
            so that the renderPos can be used in
            base class update functions """
        self.renderPos = offset + self.offset

        if self.centered:  # Center the image on the pos
            self.renderPos -= self.size / 2

    def render(self, window: Window, image: pygame.Surface = None) -> None:
        """ Renders the image to the given window """
        image = image if image is not None else self.image

        if image is not None:
            window.render(image, self.renderPos)

    # Getters
    def getSize(self) -> Vect: return self.size
    def getOffset(self) -> Vect: return self.offset
    def getRenderPos(self) -> Vect: return self.renderPos

    # Setters
    def setOffset(self, offset: Vect) -> None: self.offset = offset

    def setImg(self, image: pygame.Surface) -> None:
        self.image = image
        self.size = Vect(image.get_size())

    def setSize(self, size: Vect) -> None: self.size = size
