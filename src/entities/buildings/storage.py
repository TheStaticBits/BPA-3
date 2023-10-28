from src.entities.buildings.baseBuilding import BaseBuilding
from src.utility.vector import Vect
from src.tileset import Tileset
from src.utility.advDict import AdvDict
from src.entities.player import Player


class Storage(BaseBuilding):
    def __init__(self, type: str, tileset: Tileset, tilePos: Vect) -> None:
        super().__init__(type, tileset, tilePos)

        data: dict = self.getData()

        # The amount that the storage can store
        self.storage: AdvDict = AdvDict(data["storage"])

        self.incrementStorage()

    def incrementStorage(self) -> None:
        """ Add storage amount to the player's resource limit """
        Player.resLimits += self.storage

    def onRemove(self) -> None:
        self.decrementStorage()

    def decrementStorage(self) -> None:
        """ Remove storage amount from the player's resource limit"""
        Player.resLimits -= self.storage
