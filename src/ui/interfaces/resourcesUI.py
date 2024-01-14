import logging
from math import floor

from src.ui.interfaces.baseUI import BaseUI
from src.ui.elements.text import Text
from src.entities.player import Player
from src.window import Window


class ResourcesUI(BaseUI):
    """ Handles UI surrounding the screen
        when walking around during gameplay """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__("resourcesUI")

    def update(self, window: Window, waveNum: int) -> None:
        """ Updates the UI, resources shown, and the wave number """
        super().update(window)

        self.updateResources()
        self.updateWaveNum(waveNum)

    def updateResources(self) -> None:
        """ Update all the resources
            with the current player resource values """
        for resource in Player.resources.getPyDict().keys():
            # Get text element for the resource
            element: Text = super().getElement(resource + "Text")

            # The current number of resources
            text: str = str(floor(Player.resources[resource]))

            # If there is a limit, add it to the text
            if Player.resLimits[resource] >= 0:
                text += "/" + str(Player.resLimits[resource])

            text += " " + Player.RES_LABELS[resource]

            # Set text element's value
            element.setText(text)

    def updateWaveNum(self, waveNum: int) -> None:
        """ Sets the wave number displayed """
        super().getElement("waveText").setText(f"Wave {waveNum + 1}")
