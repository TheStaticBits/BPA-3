import pygame

from src.ui.interfaces.baseUI import BaseUI

from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.entity import Entity


class BuildingShop(BaseUI):
    """ Handles building shop UI """

    def __init__(self) -> None:
        super().__init__("buildings/shop", __name__)

        # Image scaler for building images
        self.buildingScale = super().getData()["buildingImgScale"]

        self.buildingShown: int = 0
        self.detailUIs: list[BaseUI] = []
        self.totalBuildings: int = len(BaseBuilding.BUILDINGS_DATA)

        # Load the first building shop UI
        self.loadBuildingUI(self.buildingShown, "visible")

        # Surface used to clip off the detail UIs
        # and hide them when they're not displayed over the shop
        clipSurf = pygame.Surface(super().getSize().toTuple(), pygame.SRCALPHA)
        self.clipSurface: Image = Image(surf=clipSurf, scale=False)

    def loadBuildingUI(self, index: int, posType: str) -> None:
        """ Loads the UI, images, descriptions, etc. for the building """
        if index < len(self.detailUIs):
            return  # UI already loaded

        name: str
        data: dict
        name, data = list(BaseBuilding.BUILDINGS_DATA.items())[index]

        self.log.info(f"Loading shop details for building {name}")

        buildingUI: BaseUI = BaseUI("buildings/details", __name__)
        buildingUI.getElement("buildingName").setText(name)
        buildingUI.setPosType(posType)

        # Get building image and set it
        buildingImg: Image = Entity.loadAnim(data["anim"]).getFrame(0)
        size: Vect = buildingImg.getSize() * self.buildingScale

        # Scale image and set it to the building image element
        buildingImg.transform(size)
        buildingUI.getElement("buildingImg").setImg(buildingImg)

        # Add to the list of UIs
        self.detailUIs.append(buildingUI)

    def update(self, window: Window) -> None:
        super().update(window)

        self.updateButtons()
        self.checkLeftRight()
        self.updateDetailUIs(window)

    def updateButtons(self) -> None:
        """ Updates the buttons """
        if super().getElement("openShop").getActivated():
            if super().getPosType() == "hidden":
                super().startTransition("visible")
            else:
                super().startTransition("hidden")

    def checkLeftRight(self) -> None:
        """ Checks left & right buttons and starts UI transitions
            if either are pressed"""
        if super().getElement("left").getActivated():
            if self.buildingShown == 0:
                return  # Can't go left any further

            # Start transitions for the current and next building
            self.detailUIs[self.buildingShown].startTransition("right")
            self.buildingShown -= 1
            self.detailUIs[self.buildingShown].startTransition("visible")

        # Check if the right button was pressed
        elif super().getElement("right").getActivated():
            if self.buildingShown >= self.totalBuildings - 1:
                return  # Can't go right any further

            # Start transitions for the current and next building
            self.detailUIs[self.buildingShown].startTransition("left")
            self.buildingShown += 1
            self.loadBuildingUI(self.buildingShown, "right")
            self.detailUIs[self.buildingShown].startTransition("visible")

    def updateDetailUIs(self, window: Window) -> None:
        """ Updates the detail UIs """
        # Calculate current transition offset by finding the distance from
        # the default position of "visible"
        defaultPos: Vect = super().getUIOffset(window.getSize(), "visible")
        transitionOffset: Vect = super().getOffset() - defaultPos

        # Update every building UI
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

        # Render clipped surface at the offset to the screen
        surface.render(self.clipSurface, offset)
