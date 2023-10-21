from src.scenes.baseScene import BaseScene
from src.entities.building import Building
from src.utility.vector import Vect
from src.window import Window
from src.tileset import Tileset
from src.ui.interfaces.buildingsSceneUI import BuildingsSceneUI


class BuildingsScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has buildings """

    def __init__(self, mapFolderName: str) -> None:
        """ Initializes buildings list """
        super().__init__(mapFolderName, __name__)

        self.buildings: list[Building] = []
        self.buildingsSceneUI: BuildingsSceneUI = BuildingsSceneUI()

    def update(self, window: Window) -> None:
        """ Updates buildings and test for placing buildings """
        super().update(window)

        # Update buildings
        for building in self.buildings:
            building.update(window)

        if window.getJustPressed("space"):
            self.placeBuilding()

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

    def placeBuilding(self) -> None:
        """ Tests if the player can place a building and then places it """
        # Gets tile position of player
        buildingPos: Vect = super().getPlayer().getTilePos(Tileset.TILE_SIZE)

        # Test if the position is not occupied
        if Building.testPlacement("testBuilding", buildingPos,
                                  super().getTileset()):
            # Create new building object and add to the list
            newBuilding: Building = Building(super().getTileset(),
                                             "testBuilding", buildingPos)

            self.buildings.append(newBuilding)

            self.log.info(f"Placed building at {buildingPos}")
