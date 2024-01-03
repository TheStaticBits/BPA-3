import logging
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.player import Player
from src.utility.advDict import AdvDict


class Storage(BaseBuilding):
    """ Handles storage buildings """
    log = logging.getLogger(__name__)

    def __init__(self, type: str) -> None:
        self.storage: AdvDict = AdvDict({})

        super().__init__(type)

    def onPlace(self) -> None:
        """ Add storage amount to the player's resource limit """
        self.incrementStorage()

    def onUpgrade(self, levelData: dict) -> None:
        """ Loads the storage amount for the level """
        # Remove old storage amount, then add new storage amount
        self.decrementStorage()
        self.storage = AdvDict(levelData["storageAmount"])

        if super().getLevel() > 1:
            self.incrementStorage()

    def incrementStorage(self) -> None:
        """ Add storage amount to the player's resource limit """
        Player.resLimits += self.storage

    def onRemove(self) -> None:
        self.decrementStorage()

    def decrementStorage(self) -> None:
        """ Remove storage amount from the player's resource limit"""
        Player.resLimits -= self.storage
