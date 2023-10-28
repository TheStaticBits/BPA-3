from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.advDict import AdvDict


class Generator(BaseBuilding):
    """ Handles generators that generate resources """

    def __init__(self, type: str, tileset: Tileset, tilePos: Vect) -> None:
        super().__init__(type, tileset, tilePos)

        data: dict = self.getData()

        self.generate: AdvDict = AdvDict(data["generateAmount"])
        self.oneTimeGenerate: bool = data["oneTimeGenerate"]

        if self.oneTimeGenerate:
            Player.resources += self.generate

    def update(self, window: Window) -> None:
        """ Updates generator and generates resources """
        super().update(window)

        if self.oneTimeGenerate:
            return

        # Generate resources per frame
        Player.resources += self.generate * window.getDeltaTime()

        Player.capResources()

    def onRemove(self) -> None:
        """ Remove resources when removed """
        if self.oneTimeGenerate:
            Player.resources -= self.generate
