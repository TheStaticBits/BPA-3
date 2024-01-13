import pygame
import logging

from src.ui.elements.baseUIElement import BaseUIElement
from src.utility.image import Image


class Text(BaseUIElement):
    """ Handles Text in a UI """
    log = logging.getLogger(__name__)

    # Static variable that stores font objects based on their size
    # Key: font size, value: pygame.font.Font object
    fonts: dict[int, pygame.font.Font] = {}

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        try:
            cls.FONT_PATH: str = constants["game"]["font"]
        except KeyError:
            # avoid circular import
            from src.ui.interfaces.errorUI import ErrorUI
            ErrorUI.create("Unable to find game -> font in constants",
                           cls.log)

    def __init__(self, textData: dict) -> None:
        """ Loads text data and initializes """
        super().__init__(textData)

        self.text: str = textData["text"]
        self.fontSize: int = textData["fontSize"]

        # Default text color of black
        self.color: tuple[int] = (0, 0, 0)
        if "color" in textData:
            self.color = textData["color"]

        # Width before wrapping
        self.wrapLength: int = 0
        if "wrapLength" in textData:
            self.wrapLength = textData["wrapLength"] * Image.SCALE

        self.createTextImg()

    def getFontObj(self, size: int) -> pygame.font.Font:
        """ Loads font if it has not already been loaded and returns it """
        scaledSize = size * Image.SCALE

        if scaledSize not in self.fonts:
            self.log.info(f"Loading font size {scaledSize}")
            self.fonts[scaledSize] = pygame.font.Font(self.FONT_PATH,
                                                      round(scaledSize))

        return self.fonts[scaledSize]

    def createTextImg(self) -> None:
        """ Uses the text and font to draw an image,
            and then sets the image of the BaseUIElement to it. """

        font: pygame.font.Font = self.getFontObj(self.fontSize)

        # Draw image with text
        image: pygame.Surface = font.render(self.text, False, self.color,
                                            wraplength=self.wrapLength)

        # Create, transform, and set surf with text
        surf: Image = Image(surf=image, scale=False)
        super().setImg(super().transform(surf))

    # Setters
    def setText(self, newText: str) -> None:
        self.text = newText
        self.createTextImg()
