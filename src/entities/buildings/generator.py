import logging
from src.entities.buildings.baseBuilding import BaseBuilding
from src.window import Window
from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.advDict import AdvDict


class Generator(BaseBuilding):
    """ Handles generators that generate resources """
    log = logging.getLogger(__name__)

    def __init__(self, type: str) -> None:
        super().__init__(type)

        # Whether this is generated once on building creation and removed on
        # building removal, or generated over time one time every second
        self.oneTimeGenerate: bool = self.getData()["oneTimeGenerate"]

    def onUpgrade(self, levelData: dict) -> None:
        """ Loads the generator generation amount """
        self.generate: AdvDict = AdvDict(levelData["generateAmount"])

    def onPlace(self) -> None:
        if self.oneTimeGenerate:
            Player.resources += self.generate

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player) -> None:
        """ Updates generator and generates resources """
        super().update(window, camOffset, tileset, player)

        # Do not generate resources if placing or onetimegeneration
        if self.oneTimeGenerate or super().isPlacing():
            return

        # Generate resources per frame
        Player.resources += self.generate * window.getDeltaTime()

        Player.capResources()

    def onRemove(self) -> None:
        """ Remove resources when removed if it's one time generation """
        if self.oneTimeGenerate:
            Player.resources -= self.generate
