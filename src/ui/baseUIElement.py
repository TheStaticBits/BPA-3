import pygame, logging

import src.utility.utility as util

class BaseUIElement:
    """ All UI elements (text, buttons, etc.) inherit
        from this class, which handles image loading, storage, and rendering """
    
    # Static, stores all loaded images to prevent duplicates
    # Key: string (the image's path)
    # Value: pygame.Surface (the image)
    images: dict = {}
    
    def __init__(self, imgPath: str):
        self.log = logging.getLogger(__name__)

        self.image = self.loadImg(imgPath)
    

    def loadImg(self,imgPath: str):
        """ Loads an image from the given path if it has not been loaded already,
            and returns it """
        if imgPath not in BaseUIElement.images:
            self.images[imgPath] = util.loadImg(imgPath) # loads and stores
        
        return self.images[imgPath]