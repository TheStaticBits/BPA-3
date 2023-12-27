import logging
from src.utility.vector import Vect
from src.ui.interfaces.baseUI import BaseUI
from src.utility.image import Image
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.entity import Entity
from src.utility.advDict import AdvDict
from src.entities.player import Player


class ShopDetails(BaseUI):
    """ Handles individual UIs for each building in the shop """
    log = logging.getLogger(__name__)

    def __init__(self, index: int, posType: str) -> None:
        """ Loads the UI, images, descriptions, etc. for the building
            at the given index """
        super().__init__("buildings/details")
        super().setPosType(posType)

        self.load(index)

    def load(self, index: int) -> None:
        """ Loads data for the building, and sets the UI elements
            to the data """
        self.type: str
        data: dict
        self.type, data = list(BaseBuilding.BUILDINGS_DATA.items())[index]

        self.log.info(f"Loading shop details for building {self.type}")
        super().getElement("buildingName").setText(data["name"])

        # Get building anim and use the first frame of its animation
        buildingImg: Image = Entity.loadAnim(data["anim"]).getFrame(0)

        # Get scale, multiply by size, and transform it
        scale = super().getData()["buildingImgScale"]
        newSize: Vect = buildingImg.getSize() * scale
        buildingImg.transform(newSize)

        super().getElement("buildingImg").setImg(buildingImg)

        # Get description and set it
        description: str = data["description"]
        super().getElement("description").setText(description)

        # Get cost and set it
        self.cost: AdvDict = AdvDict(data["cost"])
        for resource, amount in self.cost.getPyDict().items():
            super().getElement(resource + "Cost").setText(str(amount))

    def updateResources(self) -> None:
        """ Updates the buy button's enabled/disabled status
            based on whether the play can afford the building or not """
        super().getElement("buy").setEnabled(Player.resources >= self.cost)

    def pressedBuy(self) -> bool:
        """ Returns True if the buy button was pressed """
        return super().getElement("buy").getActivated()

    def spendResources(self) -> None:
        """ Spends the resources for the building """
        Player.resources -= self.cost

    # Getters
    def getType(self) -> str:
        """ Returns the type of building """
        return self.type
