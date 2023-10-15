import pygame
import enum

from src.ui.baseUIElement import BaseUIElement

from src.utility.vector import Vect
from src.ui.elements.text import Text


class ButtonState(enum.Enum):
    inactive = 0
    hover = 1
    pressed = 2


class Button(BaseUIElement):
    """ Handles buttons in a UI """

    def __init__(self, buttonData: dict):
        """ Loads button data and initializes """
        super().__init__(Vect(buttonData["offset"]), __name__)

        self.text = Text(buttonData["textData"])

        self.buttons: dict[str, pygame.Surface] = {}

        for key, buttonPath in buttonData["images"].items():
            self.buttons[key] = self.loadImg(buttonPath)

        self.mode: str = 0
