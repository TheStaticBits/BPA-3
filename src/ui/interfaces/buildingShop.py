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

        # Surface used to clip off the detail UIs
        # and hide them when they're not displayed over the shop
        clipSurf = pygame.Surface(super().getSize().toTuple(), pygame.SRCALPHA)
        self.clipSurface: Image = Image(surf=clipSurf)

    def loadBuildingUI(self, index: int) -> None:
        """ Loads the UI, images, descriptions, etc. for the building """
        name: str
        data: dict
        name, data = list(BaseBuilding.BUILDINGS_DATA.items())[index]

        self.log.info(f"Loading shop details for building {name}")

        buildingUI: BaseUI = BaseUI("buildings/details", __name__)
        buildingUI.getElement("buildingName").setText(name)

        # Set position of building UI
        # to whether or not it is shown and where
        posType: str
        if self.buildingShown == index:
            posType = "visible"
        elif index < self.buildingShown:
            posType = "right"
        else:
            posType = "left"

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
        self.updateDetailUIs(window)

    def updateButtons(self) -> None:
        """ Updates the buttons """
        if super().getElement("openShop").getActivated():
            if super().getPosType() == "hidden":
                super().startTransition("visible")
            else:
                super().startTransition("hidden")

    def updateDetailUIs(self, window: Window) -> None:
        """ Updates the detail UIs """
        if self.buildingShown >= len(self.detailUIs):
            self.loadBuildingUI(self.buildingShown)

        for ui in self.detailUIs:
            ui.update(window)

    def render(self, surface: Window | Image) -> None:
        super().render(surface)

        self.renderDetailUIs(surface)

    def renderDetailUIs(self, surface: Window | Image) -> None:
        """ Renders detail UIs to a clipped surface
            and then renders that to the given surface """
        offset: Vect = super().getOffset()
        self.clipSurface.getSurf().fill((0, 0, 0, 0))

        for ui in self.detailUIs:
            ui.render(self.clipSurface, -offset)

        surface.render(self.clipSurface, offset)
