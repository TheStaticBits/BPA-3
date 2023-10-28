from math import floor

from src.ui.interfaces.baseUI import BaseUI
from src.ui.elements.text import Text
from src.entities.player import Player
from src.window import Window


class ResourcesUI(BaseUI):
    """ Handles UI surrounding the screen
        when walking around during gameplay """

    def __init__(self) -> None:
        super().__init__("resourcesUI.json", __name__)

    def update(self, window: Window) -> None:
        super().update(window)

        self.updateResources(window)

    def updateResources(self, window: Window) -> None:
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

            # Set text element's value
            element.setText(text)
