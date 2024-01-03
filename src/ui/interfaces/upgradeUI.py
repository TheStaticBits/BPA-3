import logging
from src.ui.interfaces.baseUI import BaseUI
from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.utility.image import Image
from src.entities.player import Player
from src.utility.advDict import AdvDict
from src.tileset import Tileset


class UpgradeUI(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__("buildings/upgrade")

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
            self.setDisplayed()

    def setDisplayed(self) -> None:
        """ Updates the display statistics for the building """
        super().getElement("maxLevelReached").setHidden(True)

        # Set level displayed
        data: dict = self.building.getData()

        super().getElement("name").setText(f"{data['name']}")
        super().getElement("level").setText(
            f"Level {self.building.getLevel()}"
        )
        super().getElement("description").setText(data["description"])
        self.sellPrice = AdvDict(data["cost"])

        # Check if the building doesn't have another level to upgrade to
        if self.building.reachedMaxLevel():
            self.setFinished()
            return

        # Update upgrade data
        upgradeData: dict = self.building.getNextLevelData()["upgrade"]

        super().getElement("upgradeDesc").setText(
            upgradeData["description"]
        )

        # Set the cost amounts for the elements
        self.upgradeCost: AdvDict = AdvDict(upgradeData["cost"])
        for resource, amount in upgradeData["cost"].items():
            super().getElement(resource + "Cost").setText(str(amount))

    def setFinished(self) -> None:
        """ Hides elements related to upgrading, and displays
            the message that the highest level has been reached """

        # Hide upgrade elements
        super().getElement("upgradeDesc").setHidden(True)
        super().getElement("upgrade").setHidden(True)
        for resource in Player.resources.getPyDict().keys():
            super().getElement(resource + "Cost").setHidden(True)
            super().getElement(resource + "Img").setHidden(True)

        # Show max level reached message
        super().getElement("maxLevelReached").setHidden(False)

    def update(self, window: Window, tileset: Tileset) -> None:
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

        # Don't continue if closed
        if super().getPosType() == "hidden":
            return

        # Close button
        if super().getElement("closeButton").getActivated():
            self.hide(window)

        # Update buttons
        self.updateUpgradeButton()
        self.updateSellButton(window, tileset)

    def updateUpgradeButton(self) -> None:
        """ Updates the buttons to be enabled/disabled based on resources """
        if super().getElement("upgrade").isHidden():
            return

        # Upgrade button
        super().getElement("upgrade").setEnabled(
            Player.resources >= self.upgradeCost
        )

        if super().getElement("upgrade").getActivated():
            Player.resources -= self.upgradeCost
            self.building.loadLevel()  # Upgrades it
            self.setDisplayed()

    def updateSellButton(self, window: Window, tileset: Tileset) -> None:
        """ Updates the sell button to be enabled/disabled based on resources
            and sells the building if pressed """
        if super().getElement("sellButton").getActivated():
            Player.resources += self.sellPrice
            self.building.setSold(tileset)
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
