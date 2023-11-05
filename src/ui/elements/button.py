import pygame

from src.ui.elements.baseUIElement import BaseUIElement

from src.utility.vector import Vect
from src.ui.elements.text import Text
from src.window import Window


class Button(BaseUIElement):
    """ Handles buttons in a UI """

    def __init__(self, buttonData: dict) -> None:
        """ Loads button data and initializes """
        super().__init__(buttonData, __name__)

        self.buttons: dict[str, pygame.Surface] = {}

        # Load all button images
        for key, buttonPath in buttonData["images"].items():
            self.buttons[key] = super().loadImg(buttonPath)

        super().setSize(Vect(self.buttons["inactive"].get_size()))

        self.text: Text = None

        # Load text data for the button
        if "textData" in buttonData:
            textData: dict = buttonData["textData"]
            textData["centered"] = True  # Text is always centered

            self.text = Text(textData)

            self.centerText()

        # Can be "inactive", "hover", or "pressed"
        self.mode: str = "inactive"

        self.activated: bool = False

    def update(self, window: Window, offset: Vect) -> None:
        """ Updates the button's mode based on mouse position """
        super().update(window, offset)

        self.updateMouseEvents(window)

        # Update text
        if self.text is not None:
            self.text.update(window, super().getRenderPos())

    def updateMouseEvents(self, window: Window) -> None:
        """ Updates the button's mode based on mouse position """
        # Reset activated (since it is only true for one frame)
        self.activated = False

        if self.mode == "pressed":
            if window.getMouseReleased("left"):  # Mouse released button
                if self.isMouseOver(window):
                    self.activated = True
                    self.mode = "hover"
                else:
                    self.mode = "inactive"

        elif self.isMouseOver(window):
            self.mode = "hover"

            if window.getMouseJustPressed("left"):  # Just pressed button
                self.mode = "pressed"

        else:
            self.mode = "inactive"

    def isMouseOver(self, window: Window) -> bool:
        """ Tests if mouse is hovering over the button """

        rect: pygame.Rect = Vect.toRect(super().getRenderPos(),
                                        super().getSize())

        return rect.collidepoint(window.getMousePos().toTuple())

    def centerText(self) -> None:
        """ Centers the button's text """
        self.text.addToOffset(super().getSize() / 2)

    def render(self, window) -> None:
        """ Renders the button """
        super().render(window, image=self.buttons[self.mode])

        if self.text is not None:
            self.text.render(window)

    # Getters
    def getActivated(self) -> bool: return self.activated
