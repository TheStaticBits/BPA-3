from src.scenes.baseScene import BaseScene
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.buildings.storage import Storage
from src.entities.buildings.generator import Generator
from src.utility.vector import Vect
from src.window import Window
from src.tileset import Tileset
from src.ui.interfaces.buildingsSceneUI import BuildingsSceneUI


class BuildingsScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has buildings """

    BUILDING_TYPES: dict = {
        "storage": Storage,
        "generator": Generator
    }

    def __init__(self, mapFolderName: str) -> None:
        """ Initializes buildings list """
        super().__init__(mapFolderName, __name__)

        self.buildings: list[BaseBuilding] = []
        self.buildingsSceneUI: BuildingsSceneUI = BuildingsSceneUI()

    def update(self, window: Window) -> None:
        """ Updates buildings and test for placing buildings """
        super().update(window)

        # Update buildings
        for building in self.buildings:
            building.update(window)

        # Player collision with buildings
        super().getPlayer().update(window, self.buildings)

        if window.getJustPressed("space"):
            self.placeBuilding("testStorage")

        if window.getJustPressed("1"):
            self.placeBuilding("testGenerator")

        if window.getJustPressed("2"):
            self.placeBuilding("testSteamGenerator")

        self.buildingsSceneUI.update(window)

    def render(self, window: Window) -> None:
        """ Renders buildings """
        super().renderTileset(window)

        # Render buildings
        for building in self.buildings:
            building.render(window, -super().getCamOffset())

        super().renderPlayer(window)

        self.buildingsSceneUI.render(window)

        super().renderUI(window)

    def placeBuilding(self, buildingType: str) -> None:
        """ Tests if the player can place a building and then places it """
        # Gets tile position of player
        buildingPos: Vect = super().getPlayer().getTilePos(Tileset.TILE_SIZE)

        # Test if the position is not occupied
        if BaseBuilding.testPlacement(buildingType, buildingPos,
                                      super().getTileset()):
            # Get building type based on the building data
            typeName = BaseBuilding.getDataFrom(buildingType)["type"]
            objType: type = self.BUILDING_TYPES[typeName]

            # Create new building object and add to the list
            newBuilding = objType(buildingType,
                                  super().getTileset(),
                                  buildingPos)

            self.buildings.append(newBuilding)

            self.log.info(f"Placed building at {buildingPos}")
