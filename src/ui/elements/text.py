import pygame

from src.ui.elements.baseUIElement import BaseUIElement


class Text(BaseUIElement):
    """ Handles Text in a UI """

    # Static variable that stores font objects based on their size
    # Key: font size (int)
    # Value: pygame.font.Font object
    fonts: dict = {}

    @classmethod
    def loadStatic(cls, constants: dict):
        cls.FONT_PATH: str = constants["game"]["font"]

    def __init__(self, textData: dict):
        """ Loads text data and initializes """
        super().__init__(textData, __name__)

        self.text: str = textData["text"]
        self.fontSize: int = textData["fontSize"]

        # Default text color of black
        self.color: tuple[int] = (0, 0, 0)
        if "color" in textData:
            self.color = textData["color"]

        self.createTextImg()

    def getFontObj(self, size: int) -> pygame.font.Font:
        """ Loads font if it has not already been loaded and returns it """
        if size not in self.fonts:
            self.log.info(f"Loading font size {size}")
            self.fonts[size] = pygame.font.Font(self.FONT_PATH, size)

        return self.fonts[size]

    def createTextImg(self) -> None:
        """ Uses the text and font to draw an image,
            and then sets the image of the BaseUIElement to it. """

        font: pygame.font.Font = self.getFontObj(self.fontSize)

        # Draw image with text
        image: pygame.Surface = font.render(self.text, False, self.color)

        super().setImg(image)

    # Setters
    def setText(self, newText: any) -> None:
        self.text = str(newText)
        self.createTextImg()
