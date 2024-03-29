import pygame
import logging

from src.ui.elements.baseUIElement import BaseUIElement

from src.utility.vector import Vect
from src.utility.image import Image
from src.ui.elements.text import Text
from src.window import Window


class Button(BaseUIElement):
    """ Handles buttons in a UI """
    log = logging.getLogger(__name__)

    def __init__(self, buttonData: dict) -> None:
        """ Loads button data and initializes """
        super().__init__(buttonData)

        self.buttons: dict[str, Image] = {}

        # Load all button images
        for key, buttonPath in buttonData["images"].items():
            self.buttons[key] = super().transform(Image(buttonPath))

        super().setImg(self.buttons["inactive"])

        self.text: Text = None

        # Load text data for the button
        if "textData" in buttonData:
            textData: dict = buttonData["textData"]
            textData["centered"] = True  # Text is always centered

            self.text = Text(textData)

            self.centerText()

        # Can be "inactive", "hover", or "pressed"
        self.mode: str = "inactive"

        self.activated: bool = False  # True if button was just clicked
        self.enabled: bool = True  # Gray out the button if False

    def update(self, window: Window, offset: Vect) -> None:
        """ Updates the button's mode based on mouse position """
        super().update(window, offset)

        # Reset activated (since it is only true for one frame)
        self.activated = False

        if super().isHidden():
            return

        self.updateMouseEvents(window)

        # Update text
        if self.text is not None:
            self.text.update(window, super().getRenderPos())

    def updateMouseEvents(self, window: Window) -> None:
        """ Updates the button's mode based on mouse position """
        if not self.enabled:
            return

        if self.mode == "pressed":
            if window.getMouseReleased("left"):  # Mouse released button
                if self.isMouseOver(window):
                    self.activated = True
                    self.setMode("hover")
                else:
                    self.setMode("inactive")

        elif self.isMouseOver(window):
            if window.getMouseJustPressed("left"):  # Just pressed button
                self.setMode("pressed")
            else:
                self.setMode("hover")

        else:
            self.setMode("inactive")

    def isMouseOver(self, window: Window) -> bool:
        """ Tests if mouse is hovering over the button """

        rect: pygame.Rect = Vect.toRect(super().getRenderPos(),
                                        super().getSize())

        return rect.collidepoint(window.getMousePos().toTuple())

    def centerText(self) -> None:
        """ Centers the button's text """
        self.text.addToOffset(super().getSize() / 2)

    def addRenderOffset(self, offset: Vect) -> None:
        """ Adds offset to text as well as calling the super().addOffset """
        super().addRenderOffset(offset)

        if self.text is not None:
            self.text.addRenderOffset(offset)

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the button """
        if super().isHidden():
            return

        if self.mode in self.buttons:
            btnImg = self.buttons[self.mode]
        else:
            btnImg = self.buttons["inactive"]

        if not self.enabled:
            grayedImg = btnImg.copy()  # Copy image
            grayedImg.tint(140, 140, 140)  # Make gray
            btnImg = grayedImg  # Set to grayed image

        super().render(surface, image=btnImg, offset=offset)

        # Render text if it exists
        if self.text is not None:
            self.text.render(surface, offset=offset)

    # Getters
    def getActivated(self) -> bool:
        """ Only true for one frame after the button is pressed """
        return self.activated

    def getHeld(self) -> bool:
        """ True if the button is held down """
        return self.mode == "pressed"

    def getText(self) -> Text: return self.text

    def getModeImg(self) -> Image:
        """ Gets the mode image or defaults to the inactive img """
        if self.mode in self.buttons:
            return self.buttons[self.mode]

        return self.buttons["inactive"]

    # Setters
    def setMode(self, mode: str) -> None:
        if self.mode == mode:
            return

        super().setImg(self.getModeImg())
        self.mode = mode

    def setEnabled(self, enabled: bool) -> None:
        """ Sets whether or not the button is enabled """
        self.enabled = enabled

        if not enabled:  # Set image to inactive
            self.setMode("inactive")
