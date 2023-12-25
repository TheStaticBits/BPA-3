import logging
from src.entities.buildings.baseBuilding import BaseBuilding
from src.entities.player import Player
from src.utility.advDict import AdvDict


class Storage(BaseBuilding):
    """ Handles storage buildings """
    log = logging.getLogger(__name__)

    def onPlace(self) -> None:
        """ Add storage amount to the player's resource limit """
        data: dict = self.getData()

        # The amount that the storage can store
        self.storage: AdvDict = AdvDict(data["storageAmount"])

        self.incrementStorage()

    def incrementStorage(self) -> None:
        """ Add storage amount to the player's resource limit """
        Player.resLimits += self.storage

    def onRemove(self) -> None:
        self.decrementStorage()

    def decrementStorage(self) -> None:
        """ Remove storage amount from the player's resource limit"""
        Player.resLimits -= self.storage
