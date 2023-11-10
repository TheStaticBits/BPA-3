import logging

from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window


class BaseUIElement:
    """ All UI elements (text, buttons, etc.) inherit
        from this class, which handles image loading,
        storage, and rendering """

    def __init__(self, data: dict, loggerName: str = __name__,
                 imgPath: str = None) -> None:
        self.log = logging.getLogger(loggerName)

        # Offset from top left corner of each UI
        self.offset: Vect = Vect(data["offset"]) * Image.SCALE

        self.centered: bool = data["centered"] if "centered" in data else False

        self.image: Image = None
        self.size: Vect = None
        self.renderPos: Vect = None

        if imgPath is not None and imgPath != "":
            self.setImg(Image(imgPath))

    def update(self, window: Window, offset: Vect) -> None:
        """ Calculates renderPos based on offset and UI offset, so that
            the renderPos can be used in child class update functions """
        self.renderPos = self.getOffset() + offset

    def addOffset(self, offset: Vect) -> None:
        """ Adds to the current frame and element's render pos """
        self.renderPos += offset

    def render(self, surface: Window | Image,
               image: Image = None) -> None:
        """ Renders the image to the given window or surf
            with optional offset and image """
        image = image if image is not None else self.image

        surface.render(image, self.renderPos)

    def getOffset(self) -> Vect:
        """ Gets offset, accounting for
            whether or not the image is centered """
        if self.centered:
            return self.offset - self.size / 2

        return self.offset

    # Getters
    def getSize(self) -> Vect: return self.size
    def getRenderPos(self) -> Vect: return self.renderPos
    def hasImg(self) -> bool: return self.image is not None

    # Setters
    def setOffset(self, offset: Vect) -> None: self.offset = offset
    def addToOffset(self, offset: Vect) -> None: self.offset += offset

    def setImg(self, image: Image) -> None:
        self.image = image
        self.size = self.image.getSize()

    def setSize(self, size: Vect) -> None: self.size = size
