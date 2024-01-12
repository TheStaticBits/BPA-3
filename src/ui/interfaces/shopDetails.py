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

        # Building height after scaling
        self.buildingScaledHeight = super().getData()["buildingImgHeight"] * \
            Image.SCALE

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

        # Find the percentage to scale the building image by
        scale = self.buildingScaledHeight / buildingImg.getSize().y
        newSize: Vect = buildingImg.getSize() * scale
        buildingImg.transform(newSize)

        # Moves all elements in the UI over by the building image size
        self.moveElementsBy(Vect(buildingImg.getSize().x, 0))

        # Sets the building image element to the new image
        super().getElement("buildingImg").setImg(buildingImg)

        # Get description and set it
        description: str = data["description"]
        super().getElement("description").setText(description)

        # Get cost and set it
        self.cost: AdvDict = AdvDict(data["cost"])
        for resource, amount in self.cost.getPyDict().items():
            super().getElement(resource + "Cost").setText(str(amount))

    def moveElementsBy(self, amount: Vect) -> None:
        """ Moves all UI elements by the given amount,
            besides the background and building image """
        for key, element in super().getAllElements().items():
            if key != "bg" and key != "buildingImg":
                element.addToOffset(amount)

    def updateResources(self) -> None:
        """ Updates the buy button's enabled/disabled status
            based on whether the play can afford the building or not """
        super().getElement("buy").setEnabled(Player.resources >= self.cost)

    def pressedBuy(self) -> bool:
        """ Returns True if the buy button was pressed """
        return super().getElement("buy").getActivated()

    def setBuyEnabled(self, enabled: bool) -> None:
        """ Sets the state of the buy button """
        super().getElement("buy").setEnabled(enabled)

    def spendResources(self) -> None:
        """ Spends the resources for the building """
        Player.resources -= self.cost

    # Getters
    def getType(self) -> str:
        """ Returns the type of building """
        return self.type
