from src.utility.vector import Vect
from src.ui.interfaces.baseUI import BaseUI
from src.utility.image import Image
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.entity import Entity


class ShopDetails(BaseUI):
    """ Handles individual UIs for each building in the shop """

    def __init__(self, index: int, posType: str) -> None:
        """ Loads the UI, images, descriptions, etc. for the building
            at the given index """
        super().__init__("buildings/details", __name__)
        super().setPosType(posType)

        self.load(index)

    def load(self, index: int) -> None:
        """ Loads data for the building, and sets the UI elements
            to the data """
        name: str
        data: dict
        name, data = list(BaseBuilding.BUILDINGS_DATA.items())[index]

        self.log.info(f"Loading shop details for building {name}")
        super().getElement("buildingName").setText(name)

        # Get building image and set it
        buildingImg: Image = Entity.loadAnim(data["anim"]).getFrame(0)

        # Get scale, multiply by size, and transform it
        scale = super().getData()["buildingImgScale"]
        size: Vect = buildingImg.getSize() * scale
        buildingImg.transform(size)

        super().getElement("buildingImg").setImg(buildingImg)
