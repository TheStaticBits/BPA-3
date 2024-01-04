import logging
from src.scenes.baseScene import BaseScene
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.buildings.storage import Storage
from src.entities.buildings.generator import Generator
from src.entities.buildings.spawner import Spawner
from src.window import Window
from src.utility.image import Image
from src.ui.interfaces.buildingShop import BuildingShop
from src.ui.interfaces.upgradeUI import UpgradeUI


class BuildingsScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has buildings """
    log = logging.getLogger(__name__)

    # Matches a building type with the class
    BUILDING_TYPES: dict[str, type] = {
        "storage": Storage,
        "generator": Generator,
        "spawner": Spawner
    }

    def __init__(self, mapFolderName: str) -> None:
        """ Initializes buildings list """
        super().__init__(mapFolderName)

        self.buildings: list[BaseBuilding] = []
        self.buildingShop: BuildingShop = BuildingShop()
        self.upgradeUI: UpgradeUI = UpgradeUI()  # Upgrade buildings

        self.placingBuilding: bool = False

    def update(self, window: Window) -> None:
        """ Updates buildings and test for placing buildings """
        super().updateCameraPos(window)
        super().updateTileset(window)
        super().updateParticles(window)

        self.buildingShop.update(window)
        self.updateBuildings(window)
        self.updatePlayerAndUpgrades(window)

        # Makes sure the player can only buy one building at a time
        if not self.placingBuilding:
            self.testBuyBuilding()
        else:
            self.placingBuilding = self.isPlacingBuilding()

    def updateBuildings(self, window: Window) -> None:
        """ Updates all buildings """
        for building in self.buildings:
            building.update(window, super().getCamOffset(),
                            super().getTileset(), super().getPlayer())

            # Particles
            if building.isSpawningParticles():
                super().addParticles(building.getParticles())

        # Remove buildings that were sold
        self.buildings[:] = [
            building for building in self.buildings
            if not building.isSold()
        ]

    def updatePlayerAndUpgrades(self, window: Window) -> None:
        """ Updates the player and the upgrade UI,
            including the building shop and upgrade UI interactions """
        # Player collision with buildings
        player = super().getPlayer()
        collided = player.update(window, super().getTileset(),
                                 buildings=self.buildings)
        # Set upgrade UI with the selected building
        self.upgradeUI.setBuilding(collided, window)

        self.upgradeUI.update(window, super().getTileset())

        # Hide shop if the player is placing a building
        if not self.upgradeUI.canShowShop(window):
            # Hides the upgrade UI if the player just opened it
            # otherwise, hides the shop
            if self.buildingShop.startedVisible():
                self.upgradeUI.hide(window)
            else:
                self.buildingShop.hide(window)

    def testBuyBuilding(self) -> None:
        """ Tests if the player has begun placing a building """
        # Test if the player pressed the button to buy a building
        type: str = self.buildingShop.pressedBuy()
        if type:
            # Place the building
            self.log.info(f"Started placing building {type}")
            self.buildingShop.setPlacing(True)
            self.placeBuilding(type)
            self.placingBuilding = True

    def placeBuilding(self, buildingType: str) -> None:
        """ Appends building to the list """
        # Get building class from type string and building data
        typeName = BaseBuilding.getDataFrom(buildingType)["type"]
        objType: type = self.BUILDING_TYPES[typeName]

        # Create new building object and add to the list
        newBuilding: objType = objType(buildingType)
        self.buildings.append(newBuilding)

    def isPlacingBuilding(self) -> bool:
        """ Test if the user is placing a building """
        for building in self.buildings:
            if building.isPlacing():
                return True

        self.buildingShop.setPlacing(False)
        return False

    def render(self, surface: Window | Image) -> None:
        """ Renders the building scene in order """
        super().renderTileset(surface)
        super().renderParticles(surface)

        # Render buildings
        for building in self.buildings:
            building.render(surface, -super().getCamOffset())

        super().renderPlayer(surface)

        # Render UIs
        self.buildingShop.render(surface)
        self.upgradeUI.render(surface)
