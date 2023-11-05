import logging
import os

from src.window import Window
import src.utility.utility as util
from src.utility.vector import Vect

from src.ui.elements.baseUIElement import BaseUIElement
from src.ui.elements.text import Text
from src.ui.elements.button import Button


class BaseUI:
    """ All UI interfaces inherit from this class,
        which creates and handles UI elements given
        the JSON data for them. """

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
        cls.UI_FOLDER: str = constants["game"]["uiFolder"]

    def __init__(self, jsonFile: str, loggerName: str = __name__) -> None:
        self.log = logging.getLogger(loggerName)

        self.hidden: bool = False

        # Load the UI's JSON data
        jsonPath: str = os.path.join(self.UI_FOLDER, jsonFile + ".json")
        jsonData = util.loadJSON(jsonPath)

        # Dict storing all UI element objects
        # Key: string ID provided in the JSON
        # Value: UI element object (inherited from BaseUIElement)
        self.elements: dict = self.loadUI(jsonData)

        # Additional UI data
        if jsonData["size"] == "auto":
            self.size: Vect = self.findSize()
        else:
            self.size: Vect = Vect(jsonData["size"])

        self.loadPos(jsonData["positions"], jsonData["defaultPos"])

        # Load transition data if applicable
        self.transitioning: bool = False
        if "transitionSpeed" in jsonData:
            self.transitionSpeed: float = jsonData["transitionSpeed"]
            # ease or linear:
            self.transitionType: str = jsonData["transitionType"]
            self.transitionOffset: Vect = Vect(0, 0)
            # The position type to transition to
            self.transitionTo: str = self.posType

    def loadUI(self, jsonData: dict) -> dict:
        """ Loads the UI objects (text, buttons, etc.)
            from the JSON data, and returns it """
        elements: dict = {}

        for key, imageData in jsonData["elements"]["images"].items():
            elements[key] = BaseUIElement(imageData, imgPath=imageData["path"])

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

    def loadPos(self, posData: dict, defaultPos: str) -> None:
        """ Loads the position lamdas using JSON data """

        self.posType: str = defaultPos
        self.posData: dict = {}

        # Iterate through all position types and load position lamdas
        # along with the position type's margins
        for posType, posData in posData.items():
            self.posData[posType] = {}

            # loading position lambdas
            xCalc: callable = self.POS_CALCS[posData["x"]["locked"]]
            yCalc: callable = self.POS_CALCS[posData["y"]["locked"]]

            self.posData[posType]["posCalcs"] = Vect(xCalc, yCalc)

            # loading margin from JSON data
            self.posData[posType]["margin"] = Vect(
                posData["x"]["margin"], posData["y"]["margin"]
            ) * Window.IMG_SCALE

    def update(self, window: Window) -> None:
        """ Updates all elements """
        if self.hidden:
            return

        offset: Vect = self.getUIOffset(window, self.posType)

        # Apply transitioning offset if applicable
        if self.transitioning:
            self.updateTransition(offset, window)
            offset += self.transitionOffset

        # Iterate through UI elements and update them
        for element in self.elements.values():
            element.update(window, offset)

    def getUIOffset(self, window: Window, posType: str) -> Vect:
        """ Gets the offset of the UI interface based on the position type """

        posCalcs: Vect = self.posData[posType]["posCalcs"]  # lamdas
        margin: Vect = self.posData[posType]["margin"]

        # Calculate UI interface offset based on position lambdas
        return Vect(
            posCalcs.x(window.getWindowSize().x, self.size.x, margin.x),
            posCalcs.y(window.getWindowSize().y, self.size.y, margin.y)
        )

    def updateTransition(self, oldOffset: Vect, window: Window) -> None:
        """ Updates the UI's transition """
        # Get the offset of the UI interface based on the transition to type
        newOffset: Vect = self.getUIOffset(window, self.transitionTo)

        # Calculate the offset diff,
        # This is what the self.transitionOffset needs to move to
        offsetDiff: Vect = newOffset - oldOffset

        moveAmount: Vect
        if self.transitionType == "ease":
            # Moves the transition over time, slowing down near the end
            # Same logic used for camera movement centering the player
            moveAmount = (offsetDiff - self.transitionOffset) * \
                self.transitionSpeed * window.getDeltaTime() * Window.IMG_SCALE
        else:
            # Moves transition linearly
            moveAmount = offsetDiff.getSigns() * self.transitionSpeed * \
                window.getDeltaTime() * Window.IMG_SCALE

        # Move the transition offset by the move amount
        self.transitionOffset += moveAmount

        # If the transition offset has roughly reached the new offset,
        # set the transition offset to the new offset and stop transitioning
        if self.transitionDone(offsetDiff):
            self.log.info(f"UI Transition to {self.transitionTo} complete")

            self.transitioning = False
            self.transitionOffset = offsetDiff
            self.posType = self.transitionTo

    def transitionDone(self, moveTo: Vect) -> bool:
        """ Returns whether or not the UI has reached
            the end of its transition """
        if self.transitionType == "ease":
            return moveTo == self.transitionOffset.round()

        # linear transition animation testing, which
        # tests if the UI has moved past its destination offset
        return not moveTo.signsMatch(moveTo - self.transitionOffset)

    def startTransition(self, window: Window, posType: str) -> None:
        """ Starts UI transition to the given position type """
        if self.transitionTo == posType:
            return

        if not self.transitioning:
            self.transitioning = True
            self.transitionOffset = Vect(0, 0)

        self.transitionTo = posType

    def render(self, window: Window) -> None:
        """ Renders all UI elements in this interface """
        if self.hidden:
            return

        for element in self.elements.values():
            element.render(window)

    # Getters
    def getElement(self, key: str) -> BaseUIElement:
        return self.elements[key]

    def isTransitioning(self) -> bool:
        return self.transitioning

    def getPosType(self) -> str:
        return self.transitionTo

    # Setters
    def setHidden(self, hidden: bool) -> None:
        self.hidden = hidden
