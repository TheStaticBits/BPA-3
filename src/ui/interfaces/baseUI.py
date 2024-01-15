import logging
import os
from typing import Callable

import src.utility.utility as util
from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window
from src.utility.overlay import Overlay

from src.ui.elements.baseUIElement import BaseUIElement
from src.ui.elements.text import Text
from src.ui.elements.button import Button


class BaseUI:
    """ All UI interfaces inherit from this class,
        which creates and handles UI elements given
        the JSON data for them. """
    log = logging.getLogger(__name__)

    # Given a window size (int), UI size (int), and margin (int),
    # these return the position of each UI interface
    # for each of the three alignments
    POS_CALCS: dict[str, Callable[[int, int, int], int]] = {
        "start": lambda windowSize, uiSize, margin:
        margin,

        "center": lambda windowSize, uiSize, margin:
        (windowSize - uiSize) / 2 + margin,

        "end": lambda windowSize, uiSize, margin:
        windowSize - uiSize - margin
    }

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Load static vars from constants """
        try:
            cls.UI_FOLDER: str = constants["game"]["uiFolder"]
        except KeyError:
            # avoid circular import
            from src.ui.interfaces.errorUI import ErrorUI
            ErrorUI.create("Unable to find game -> uiFolder in constants",
                           cls.log)

    def __init__(self, jsonFile: str) -> None:
        # Load the UI's JSON data
        self.data = self.loadJson(jsonFile)
        self.name = jsonFile

        # Dict storing all UI element objects
        # Key: string ID provided in the JSON
        # Value: UI element object (inherited from BaseUIElement)
        self.elements: dict[str, BaseUIElement] = self.loadUI(self.data)

        # Additional UI data
        if self.data["size"] == "auto":
            self.size: Vect = self.findSize()
        else:
            self.size: Vect = Vect(self.data["size"]) * Image.SCALE

        if "bgAlpha" in self.data:
            # Adds an overlay in the background when the position is the type
            self.overlay = Overlay(self.data["bgAlpha"])
            self.bgAlphaPosType: str = self.data["bgAlphaShowsPos"]
        else:
            self.overlay = None

        # Get layer number if provided in the data
        self.layers: int = self.data["layers"] if "layers" in self.data else 1

        self.loadPosTypes(self.data["positions"],
                          self.data["defaultPos"])
        self.loadTransitionData(self.data)

        # Percent done transitioning
        self.percentDone: float = 1
        # Distance between transition offsets
        # used to calculate percent done:
        self.transitionDist: float = 0

    def loadJson(self, jsonFile: str) -> dict:
        """ Loads the UI's JSON data """
        jsonPath: str = os.path.join(self.UI_FOLDER, jsonFile + ".json")
        return util.loadJSON(jsonPath)

    def loadUI(self, jsonData: dict) -> dict:
        """ Loads the UI objects (text, buttons, etc.)
            from the JSON data, and returns it """
        elements: dict = {}

        # avoid circular import
        from src.ui.interfaces.errorUI import ErrorUI
        try:
            # Load image elements from the UI JSON data
            # by using the base UI element object
            for key, imageData in jsonData["elements"]["images"].items():
                elements[key] = BaseUIElement(imageData,
                                              imgPath=imageData["path"])

            # Load text elements from the UI JSON data
            for key, textData in jsonData["elements"]["text"].items():
                elements[key] = Text(textData)

            # Load button elements
            for key, buttonData in jsonData["elements"]["buttons"].items():
                elements[key] = Button(buttonData)
        except KeyError:
            ErrorUI.create("Unable to find elements -> [images, text, or "
                           "buttons] in UI JSON", self.log,
                           recoverable=True)

        return elements

    def findSize(self) -> Vect:
        """ Finds the size of the UI interface from the elements """
        # Find the object with the greatest offset + size
        # from the UI's top left corner. This is the size of the UI
        greatest: Vect = Vect(0, 0)

        # Iterate through all elements in the UI
        for element in self.elements.values():
            if not element.hasImg():  # Must have an image to test it
                continue

            # Find bottom right render coordinate of element within the UI
            bottomRight: Vect = element.getSize() + element.getOffset()
            if bottomRight >= greatest:
                greatest = bottomRight

        return greatest

    def loadPosTypes(self, posData: dict, defaultPos: str) -> None:
        """ Loads the position lamdas and other data
            for each position type using the UI JSON data """

        self.posType: str = defaultPos
        self.posData: dict = {}

        # Iterate through all position types and load position lamdas
        # along with the position type's other data like margins
        for posType, posData in posData.items():
            self.posData[posType] = {}

            # loading position lambdas
            xCalc: Callable = self.POS_CALCS[posData["x"]["locked"]]
            yCalc: Callable = self.POS_CALCS[posData["y"]["locked"]]

            self.posData[posType]["posCalcs"] = (xCalc, yCalc)

            # loading margin from JSON data
            self.posData[posType]["margin"] = Vect(
                posData["x"]["margin"], posData["y"]["margin"]
            ) * Image.SCALE

            # Set hidden value to false if not provided
            hidden: bool = posData["hidden"] if "hidden" in posData else False
            self.posData[posType]["hidden"] = hidden

        # Set hidden to default pos type's hidden value
        self.hidden = self.posData[self.posType]["hidden"]

    def loadTransitionData(self, jsonData: dict) -> None:
        """ Loads transition data from the UI JSON data if applicable """
        self.transitioning: bool = False
        if "transitionSpeed" in jsonData:
            # speed of transitions, divided by image scale to
            # maintain it across different scales
            self.transitionSpeed: float = jsonData["transitionSpeed"] / \
                Image.SCALE
            # ease or linear:
            self.transitionType: str = jsonData["transitionType"]
            self.transitionOffset: Vect = Vect(0, 0)
            # The position type to transition to
            self.transitionTo: str = self.posType

    def update(self, window: Window, offset: Vect = Vect()) -> None:
        """ Updates all elements, transition, and offsets """
        # Temporary offset for each frame
        # Setting it to the original offset (without transition offset yet)
        self.offset = self.getUIOffset(window.getSize(), self.posType)

        # Apply transitioning offset if applicable
        if self.transitioning:
            self.updateTransition(window, self.offset)
            self.offset += self.transitionOffset

        self.offset += offset

        # Don't update UI elements if hidden
        if self.hidden:
            return

        # Iterate through UI elements and update them with the offset
        for element in self.elements.values():
            element.update(window, self.offset)

        self.updateOverlay(window)

    def getUIOffset(self, surfaceSize: Vect, posType: str) -> Vect:
        """ Gets the offset of the UI interface based on the position type """

        posCalcs: Vect = self.posData[posType]["posCalcs"]  # lamdas
        margin: Vect = self.posData[posType]["margin"]

        # Calculate UI interface offset using lambda position calculators
        # These are finding the "start", "center", or "end" position for x & y
        return Vect(
            posCalcs[0](surfaceSize.x, self.size.x, margin.x),
            posCalcs[1](surfaceSize.y, self.size.y, margin.y)
        )

    def updateTransition(self, window: Window, oldOffset: Vect) -> None:
        """ Updates the UI's transition """
        # Get the offset of the UI interface based on the transition to type
        newOffset: Vect = self.getUIOffset(window.getSize(), self.transitionTo)

        # Calculate the offset diff,
        # This is what the self.transitionOffset needs to move to
        offsetDiff: Vect = newOffset - oldOffset

        moveAmount: Vect
        if self.transitionType == "ease":
            # Moves the transition over time, slowing down near the end
            # Same logic used for camera movement centering the player
            moveAmount = (offsetDiff - self.transitionOffset) * \
                self.transitionSpeed * window.getDeltaTime() * Image.SCALE
        else:
            # Moves transition linearly
            moveAmount = offsetDiff.getSigns() * self.transitionSpeed * \
                window.getDeltaTime() * Image.SCALE

        # Move the transition offset by the move amount
        self.transitionOffset += moveAmount

        # Calculate percent done with a transition by finding
        # the distance between the transition offset and the new offset
        # and dividing it by the distance between the new offset and the old
        self.percentDone = self.transitionOffset.dist(offsetDiff)
        self.percentDone /= self.transitionDist
        self.percentDone = 1 - self.percentDone

        # If the transition offset has roughly reached the new offset,
        # set the transition offset to the new offset and stop transitioning
        if self.transitionDone(offsetDiff):
            self.log.info(
                f'UI "{self.name}" Transition to {self.transitionTo} complete'
            )

            self.transitioning = False
            self.transitionOffset = offsetDiff
            self.posType = self.transitionTo
            self.hidden = self.posData[self.posType]["hidden"]

    def transitionDone(self, moveTo: Vect) -> bool:
        """ Returns whether or not the UI has reached
            the end of its transition """
        if self.transitionType == "ease":
            return moveTo == self.transitionOffset.round()

        # linear transition animation testing, which
        # tests if the UI has moved past its destination offset
        return not moveTo.signsMatch(moveTo - self.transitionOffset)

    def updateOverlay(self, window: Window) -> None:
        """ Updates the overlay if applicable """
        if self.overlay is None:
            return

        # Transitioning, so get opacity based on the percent done
        if self.transitioning:
            reversed: bool = self.transitionTo != self.bgAlphaPosType
            opacity: int = self.overlay.percentOpacity(self.percentDone,
                                                       reversed)
        elif self.posType == self.bgAlphaPosType:
            opacity: int = -1  # Max opacity
        else:
            opacity: int = 0

        self.overlay.update(opacity, window)

    def startTransition(self, posType: str, surface: Window | Image) -> None:

        """ Starts UI transition to the given position type """
        if self.transitionTo == posType:
            return  # Already at or transitioning to this pos type

        if not self.transitioning:
            self.transitioning = True
            self.transitionOffset = Vect(0, 0)  # Reset transition offset

        # Calculate the distance between the old and new offsets
        oldOffset: Vect = self.getUIOffset(surface.getSize(),
                                           self.transitionTo)
        newOffset: Vect = self.getUIOffset(surface.getSize(),
                                           posType)
        self.transitionDist = newOffset.dist(oldOffset)

        # Set the transition to position type
        self.transitionTo = posType
        self.hidden = False  # Always show UI while transitioning

    def render(self, surface: Window | Image,
               offset: Vect = Vect()) -> None:
        """ Renders all UI elements in this interface """
        if self.hidden:
            return

        if self.overlay is not None:
            self.overlay.render(surface)

        # Render all elements in the order of layers
        for layer in range(self.layers):
            self.renderLayer(surface, layer, offset)

    def renderLayer(self, surface: Window | Image,
                    layer: int, offset: Vect = Vect()) -> None:
        """ Renders all elements in the given layer """
        for element in self.elements.values():
            if element.getLayer() != layer:
                continue

            element.render(surface, offset=offset)

    def findDistFromPos(self, posType: str, window: Window) -> Vect:
        """ Returns the distance between the given position type
            and the current position """
        position: Vect = self.getUIOffset(window.getSize(), posType)
        return self.offset - position

    # Getters
    def getElement(self, key: str) -> BaseUIElement:
        return self.elements[key]

    def isTransitioning(self) -> bool: return self.transitioning
    def isHidden(self) -> bool: return self.hidden

    def getAllElements(self) -> dict[str, BaseUIElement]: return self.elements
    def getPosType(self) -> str: return self.transitionTo
    def getSize(self) -> Vect: return self.size
    def getData(self) -> dict: return self.data
    def getOffset(self) -> Vect: return self.offset
    def getTransitionOffset(self) -> Vect: return self.transitionOffset
    def getPercentDone(self) -> float: return self.percentDone

    # Setters
    def setHidden(self, hidden: bool) -> None:
        self.hidden = hidden

    def setPosType(self, posType: str) -> None:
        """ Directly change pos type without activating a transition """
        self.posType = posType
        self.hidden = self.posData[posType]["hidden"]
        self.transitionTo = posType
