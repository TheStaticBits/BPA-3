import logging
import os

from src.window import Window
import src.utility.utility as util
from src.utility.vector import Vect

from src.ui.baseUIElement import BaseUIElement
from src.ui.elements.text import Text
from src.ui.elements.button import Button


class BaseUI:
    """ All UI interfaces inherit from this class,
        which creates and handles UI elements given
        the JSON data for them. """

    UI_FOLDER: str = None

    # Given a window size (int), UI size (int), and margin (int),
    # these return the position of each UI interface
    # for each of the three alignments
    POS_CALCS: dict = {
        "start": lambda windowSize, uiSize, margin:
        margin,

        "center": lambda windowSize, uiSize, margin:
        (windowSize - uiSize) / 2 + margin,

        "end": lambda windowSize, uiSize, margin:
        windowSize - uiSize - margin
    }

    @classmethod
    def loadStatic(cls, constants: dict):
        """ Load static vars from constants """
        cls.UI_FOLDER = constants["game"]["uiFolder"]

    def __init__(self, jsonFile: str, loggerName: str = __name__) -> None:
        self.log = logging.getLogger(loggerName)

        # Load the UI's JSON data
        jsonData = util.loadJSON(os.path.join(self.UI_FOLDER, jsonFile))

        # Dict storing all UI element objects
        # Key: string ID provided in the JSON
        # Value: UI element object (inherited from BaseUIElement)
        self.elements: dict = self.loadUI(jsonData)

        # Additional UI data
        if jsonData["size"] == "auto":
            self.size: Vect = self.findSize()
        else:
            self.size: Vect = Vect(jsonData["size"])

        self.loadPos(jsonData["pos"])

    def loadUI(self, jsonData: dict) -> dict:
        """ Loads the UI objects (text, buttons, etc.)
            from the JSON data, and returns it """
        elements: dict = {}

        for key, imageData in jsonData["elements"]["images"].items():
            elements[key] = BaseUIElement(imageData, "src.ui.baseUIElement",
                                          imageData["path"])

        for key, textData in jsonData["elements"]["text"].items():
            elements[key] = Text(textData)

        for key, buttonData in jsonData["elements"]["buttons"].items():
            elements[key] = Button(buttonData)

        return elements

    def findSize(self) -> Vect:
        """ Finds the size of the UI object from the elements """
        # Find the object with the greatest offset + size
        # from the UI's top left corner. This is the size of the UI
        greatest: Vect = Vect(0, 0)

        for element in self.elements.values():
            bottomRight: Vect = element.getSize() + element.getOffset()
            if bottomRight >= greatest:
                greatest = bottomRight

        return greatest

    def loadPos(self, posData: dict) -> None:
        """ Loads the position lamdas using JSON data """

        self.xPos: callable = self.POS_CALCS[posData["x"]["locked"]]
        self.yPos: callable = self.POS_CALCS[posData["y"]["locked"]]

        self.margin: Vect = Vect(posData["x"]["margin"],
                                 posData["y"]["margin"])

    def update(self, window: Window) -> None:
        """ Updates all elements """

        # Calculate UI interface offset based on position lambdas
        offset: Vect = Vect(
            self.xPos(window.getWindowSize().x, self.size.x, self.margin.x),
            self.yPos(window.getWindowSize().y, self.size.y, self.margin.y)
        )

        # Iterate through UI elements and update them
        for element in self.elements.values():
            element.update(window, offset)

    def render(self, window: Window) -> None:
        """ Renders all UI elements in this interface """

        for element in self.elements.values():
            element.render(window)

    # Getters
    def getElement(self, key: str) -> BaseUIElement:
        return self.elements[key]
