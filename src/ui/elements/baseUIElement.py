import logging

from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window


class BaseUIElement:
    """ All UI elements (text, buttons, etc.) inherit
        from this class, which handles image loading,
        storage, and rendering """
    log = logging.getLogger(__name__)

    def __init__(self, data: dict, imgPath: str = None) -> None:
        # Offset from top left corner of each UI
        self.offset: Vect = Vect(data["offset"]) * Image.SCALE

        # Load optional data values
        self.centered: bool = data["centered"] if "centered" in data else False
        self.rotateDegrees: float = data["rotate"] if "rotate" in data else 0
        self.flip: Vect = Vect(data["flip"]) if "flip" in data else Vect(False)
        self.layer: int = data["layer"] if "layer" in data else 0
        self.isScaled: bool = data["scaled"] if "scaled" in data else True

        self.image: Image = None
        self.size: Vect = None
        self.renderPos: Vect = Vect(0, 0)
        self.hidden: bool = False

        if imgPath is not None and imgPath != "":
            image: Image = self.transform(Image(imgPath, scale=self.isScaled))
            self.setImg(image)

    def update(self, window: Window, offset: Vect) -> None:
        """ Calculates renderPos based on offset and UI offset, so that
            the renderPos can be used in child class update functions """
        self.renderPos = self.getOffset() + offset

    def addRenderOffset(self, offset: Vect) -> None:
        """ Adds to the current frame and element's render pos """
        self.renderPos += offset

    def render(self, surface: Window | Image,
               image: Image = None, offset: Vect = Vect()) -> None:
        """ Renders the image to the given window or surf
            with optional offset and image """
        if self.hidden:
            return

        image = image if image is not None else self.image

        surface.render(image, self.renderPos + offset)

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
    def getLayer(self) -> int: return self.layer
    def isHidden(self) -> bool: return self.hidden

    # Setters
    def setOffset(self, offset: Vect) -> None: self.offset = offset
    def addToOffset(self, offset: Vect) -> None: self.offset += offset
    def setHidden(self, hidden: bool) -> None: self.hidden = hidden

    def transform(self, image: Image) -> Image:
        """ Transforms a given image based on the element's data """
        image.rotate(self.rotateDegrees)
        image.flip(self.flip.x, self.flip.y)
        return image

    def setImg(self, image: Image) -> None:
        self.image = image
        self.size = self.image.getSize()

    def setSize(self, size: Vect) -> None: self.size = size
