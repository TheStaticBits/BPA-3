import logging

from src.ui.interfaces.baseUI import BaseUI

from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window
from src.entities.buildings.baseBuilding import BaseBuilding
from src.ui.interfaces.shopDetails import ShopDetails


class BuildingShop(BaseUI):
    """ Handles the building shop UI """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Load data, initialize, and load the first building UI """
        super().__init__("buildings/shop")

        self.buildingShown: int = 0
        self.detailUIs: list[ShopDetails] = []
        self.totalBuildings: int = len(BaseBuilding.BUILDINGS_DATA)

        # Load the first building shop UI
        self.loadBuildingUI(self.buildingShown, "visible")

        # Surface used to clip off the detail UIs
        # and hide them when they're not displayed over the shop
        self.clipSurface: Image = Image.makeEmpty(super().getSize(),
                                                  transparent=True)

        self.checkButtonsDisabled()

    def loadBuildingUI(self, index: int, posType: str) -> None:
        """ Loads the UI, images, descriptions, etc. for the building """
        if index < len(self.detailUIs):
            return  # UI already loaded

        # Load and append to list
        buildingUI = ShopDetails(index, posType)
        self.detailUIs.append(buildingUI)

    def update(self, window: Window, isPlacing: bool) -> None:
        """ Updates the UI buttons """
        super().update(window)

        self.updateButtons(window)
        self.checkLeftRight(window)
        self.updateDetailUIs(window)

        # Only check the buy button status when the player isn't
        # placing a building
        if not isPlacing:
            # Updates buy button status
            self.detailUIs[self.buildingShown].updateResources()
        else:
            # Sets the buy button state to disabled while the player
            # is placing a building
            self.detailUIs[self.buildingShown].setBuyEnabled(False)

    def updateButtons(self, window: Window) -> None:
        """ Updates the buttons """
        if super().getElement("openShop").getActivated():
            if super().getPosType() == "hidden":
                super().startTransition("visible", window)
            else:
                super().startTransition("hidden", window)

    def checkButtonsDisabled(self) -> None:
        """ Updates the disabled/enabled status of the left/right buttons
            based on whether or not there are buildings to the left/right """
        super().getElement("left").setEnabled(self.buildingShown != 0)
        super().getElement("right").setEnabled(
            self.buildingShown != self.totalBuildings - 1)

    def checkLeftRight(self, window: Window) -> None:
        """ Checks left & right buttons and starts UI transitions
            if either are pressed"""
        if super().getElement("left").getActivated():
            if self.buildingShown == 0:
                return  # Can't go left any further

            # Start transitions for the current and next building
            self.detailUIs[self.buildingShown].startTransition("right",
                                                               window)
            self.buildingShown -= 1
            self.detailUIs[self.buildingShown].startTransition("visible",
                                                               window)
            self.checkButtonsDisabled()

        # Check if the right button was pressed
        elif super().getElement("right").getActivated():
            if self.buildingShown >= self.totalBuildings - 1:
                return  # Can't go right any further

            # Start transitions for the current and next building
            self.detailUIs[self.buildingShown].startTransition("left", window)
            self.buildingShown += 1
            self.loadBuildingUI(self.buildingShown, "right")
            self.detailUIs[self.buildingShown].startTransition("visible",
                                                               window)
            self.checkButtonsDisabled()

    def updateDetailUIs(self, window: Window) -> None:
        """ Updates the detail UIs """
        # Find current distance from the visible position,
        # to use it as an offset on the detail UIs
        transitionOffset: Vect = super().findDistFromPos("visible", window)

        # Update every building UI with the transition offset
        # This means that buttons and other such elements will have the proper
        # offset based on the current height of the outer shop UI
        for ui in self.detailUIs:
            ui.update(window, transitionOffset)

    def render(self, surface: Window | Image) -> None:
        """ Renders the UI to the given surface along with the
            building shop detail UIs """
        # Render the base UI
        super().renderLayer(surface, 0)
        self.renderDetailUIs(surface)  # Render shop detail UIs
        # Render left/right buttons on top of that
        super().renderLayer(surface, 1)

    def renderDetailUIs(self, surface: Window | Image) -> None:
        """ Renders detail UIs to a clipped surface
            and then renders that to the given surface """
        offset: Vect = super().getOffset()
        self.clipSurface.getSurf().fill((0, 0, 0, 0))  # Clear surf

        for ui in self.detailUIs:
            # Render at the negative offset to clip it
            ui.render(self.clipSurface, -offset)

            # Don't clip (for testing):
            # ui.render(surface)

        # Render clipped surface at the offset to the screen
        surface.render(self.clipSurface, offset)

    def pressedBuy(self) -> str:
        """ Returns the type of building, or None if no building was bought """
        if self.detailUIs[self.buildingShown].pressedBuy():
            # Spend player resources
            self.detailUIs[self.buildingShown].spendResources()
            # Return type
            return self.detailUIs[self.buildingShown].getType()

        return None

    def hide(self, window: Window) -> None:
        """ Hides the UI """
        super().startTransition("hidden", window)

    def startedVisible(self) -> bool:
        """ Returns True if the UI has started transitioning to visible """
        return super().isTransitioning() and \
            super().getPosType() == "visible"
