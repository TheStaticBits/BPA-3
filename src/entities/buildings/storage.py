import logging
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.player import Player
from src.utility.advDict import AdvDict


class Storage(BaseBuilding):
    """ Handles storage buildings """
    log = logging.getLogger(__name__)

    def onPlace(self) -> None:
        """ Add storage amount to the player's resource limit """
        self.incrementStorage()

    def onUpgrade(self, levelData: dict) -> None:
        """ Loads the storage amount for the level """
        self.storage: AdvDict = AdvDict(levelData["storageAmount"])

    def incrementStorage(self) -> None:
        """ Add storage amount to the player's resource limit """
        Player.resLimits += self.storage

    def onRemove(self) -> None:
        self.decrementStorage()

    def decrementStorage(self) -> None:
        """ Remove storage amount from the player's resource limit"""
        Player.resLimits -= self.storage
