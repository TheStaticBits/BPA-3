import pygame, logging

import src.utility.utility as util
from src.utility.vector import Vect
from src.window import Window

class BaseUIElement:
    """ All UI elements (text, buttons, etc.) inherit
        from this class, which handles image loading, storage, and rendering """
    
    # Static, stores all loaded images to prevent duplicates
    # Key: string (the image's path)
    # Value: pygame.Surface (the image)
    images: dict = {}
    
    def __init__(self, offset: Vect, loggerName: str, imgPath: str=None) -> None:
        self.log = logging.getLogger(loggerName)

        self.offset: Vect = offset # Offset from top left corner of each UI

        self.image: pygame.Surface = None
        self.size: Vect = None

        if imgPath is not None:
            self.setImg(self.loadImg(imgPath))
    

    def loadImg(self, imgPath: str) -> pygame.Surface:
        """ Loads an image from the given path if it has not been loaded already,
            and returns it """
        if imgPath not in BaseUIElement.images:
            self.images[imgPath] = util.loadImg(imgPath) # loads and stores
        
        return self.images[imgPath]
    

    def update(self, window: Window) -> None:
        """ Override in base classes if needed """


    def render(self, window: Window, offset: Vect) -> None:
        """ Renders the image to the given window """
        if self.image is not None:
            window.render(self.image, self.offset + offset)
    

    # Getters
    def getSize(self) -> Vect: return self.size
    def getOffset(self) -> Vect: return self.offset

    # Setters
    def setImg(self, image: pygame.Surface) -> None:
        self.image = image
        self.size = Vect(image.get_size())