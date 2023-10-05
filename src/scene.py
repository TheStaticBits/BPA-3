import logging

from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.window import Window
from src.entities.building import Building

class Scene:
    """ Contains tileset, player, buildings, etc.
        Manages camera offset and other scene-related things """
    
    def __init__(self, constants: dict, mapFolderName: str) -> None:
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing scene for map " + mapFolderName)

        self.tileset: Tileset = Tileset(mapFolderName)
        self.player: Player = Player(constants, self.tileset.getPlayerStart())
        
        self.buildings: list[Building] = []

        self.cameraOffset: Vect = Vect()


    def update(self, window: Window) -> None:
        """ Update scene objects """
        self.tileset.update(window)

        # Update buildings
        for building in self.buildings:
            building.update(window)
            
        self.player.update(window)

        self.updateCameraPos(window)
        self.testPlaceBuilding(window)

    
    def updateCameraPos(self, window: Window) -> None:
        """ Update camera position """
        self.cameraOffset = self.findCameraPos(window)
    
    
    def testPlaceBuilding(self, window: Window) -> None:
        """ Temporary building placement """
        if window.getJustPressed("space"):
            buildingPos: Vect = self.player.getTilePos(Tileset.TILE_SIZE)
            
            # Test if the position is not occupied
            if Building.testPlacement("testBuilding", buildingPos, self.tileset):
                newBuilding: Building = Building(self.tileset, "testBuilding", buildingPos)
                self.buildings.append(newBuilding)

                self.log.info(f"Placed building at {buildingPos}")
    

    def render(self, window: Window) -> None:
        """ Render scene objects """
        self.tileset.render(window, -self.cameraOffset)

        # Render all buildings
        for building in self.buildings:
            building.render(window, -self.cameraOffset)
    
        self.player.render(window, -self.cameraOffset)


    def findCameraPos(self, window: Window) -> Vect:
        """ Returns the camera position """
        # Finding the camera position centered on the player
        return self.player.getCenterPos() - window.getWindowSize() / 2