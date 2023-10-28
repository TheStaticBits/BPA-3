from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.advDict import AdvDict


class Generator(BaseBuilding):
    def __init__(self, type: str, tileset: Tileset, tilePos: Vect) -> None:
        super().__init__(type, tileset, tilePos)

        data: dict = self.getData()

        self.generate: AdvDict = AdvDict(data["generateAmount"])

    def update(self, window: Window) -> None:
        """ Updates generator and generates resources """
        super().update(window)

        print(self.generate)

        Player.resources += self.generate * window.getDeltaTime()

        Player.capResources()
