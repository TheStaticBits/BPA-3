import logging
from src.ui.interfaces.baseUI import BaseUI
from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.utility.image import Image


class UpgradeUI(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__("upgradeUI")

        self.building: BaseBuilding = None

        # For if the player goes immediately from one building to another,
        # to show the transition to hidden and then back to visible.
        self.betweenBuildings: bool = False
        self.goToBuilding: BaseBuilding = None

        # The min width of the window to allow both the upgrade UI and
        # the shop UI to show at the same time. Otherwise, only one can be
        # shown at the same time.
        self.expandedMinWidth = super().getData()["expandedMinWidth"] * \
            Image.SCALE

    def setBuilding(self, building: BaseBuilding, window: Window) -> None:
        """ Sets the building to upgrade """
        if building is None or building == self.building or \
           super().isTransitioning():
            return

        # Currently already has building showing:
        if self.building is not None and super().getPosType() != "hidden":
            self.betweenBuildings = True
            self.goToBuilding = building
            super().startTransition("hidden", window)

        else:  # No building showing, so move to visible
            self.building = building
            super().startTransition("visible", window)
            self.setStats(window)

    def setStats(self, window: Window) -> None:
        """ Updates the display statistics for the building """
        pass

    def update(self, window: Window) -> None:
        """ Selects the building to make it render with a tint """
        if self.betweenBuildings and not super().isTransitioning():
            # Finished transition to hidden, so start transition to visible
            self.setBuilding(self.goToBuilding, window)
            self.betweenBuildings = False
            self.goToBuilding = None

        # Select the goToBuilding if it exists, otherwise select the building
        if self.goToBuilding is not None:
            self.goToBuilding.select()
        elif self.building is not None:
            self.building.select()

        super().update(window)

        # Close button
        if super().getElement("closeButton").getActivated():
            self.hide(window)

    def canShowShop(self, window: Window) -> bool:
        """ Returns whether or not the shop UI can be shown based on the
            upgrade UI and the window size.
            This prevents them from overlapping """
        # If the upgrade UI isn't visible:
        if not super().isTransitioning() and self.getPosType() == "hidden":
            return True

        # Test if the window is large enough to fit both UIs at once
        return window.getSize().x >= self.expandedMinWidth

    def hide(self, window: Window) -> None:
        """ Closes the upgrade menu """
        super().startTransition("hidden", window)
        self.building = None
