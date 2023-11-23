from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.advDict import AdvDict


class Generator(BaseBuilding):
    """ Handles generators that generate resources """

    def __init__(self, type: str) -> None:
        super().__init__(type)

        data: dict = self.getData()

        self.generate: AdvDict = AdvDict(data["generateAmount"])
        self.oneTimeGenerate: bool = data["oneTimeGenerate"]

    def onPlace(self) -> None:
        if self.oneTimeGenerate:
            Player.resources += self.generate

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player) -> None:
        """ Updates generator and generates resources """
        super().update(window, camOffset, tileset, player)

        if self.oneTimeGenerate or super().isPlacing():
            return

        # Generate resources per frame
        Player.resources += self.generate * window.getDeltaTime()

        Player.capResources()

    def onRemove(self) -> None:
        """ Remove resources when removed """
        if self.oneTimeGenerate:
            Player.resources -= self.generate
