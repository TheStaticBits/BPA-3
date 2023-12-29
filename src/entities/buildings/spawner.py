import logging
from src.entities.buildings.baseBuilding import BaseBuilding
from src.utility.timer import Timer
from src.window import Window
from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.scenes.dungeonScene import DungeonScene
from src.entities.warrior import Warrior


class Spawner(BaseBuilding):
    """ Handles spawner buildings that spawn ally warriors periodically """
    log = logging.getLogger(__name__)

    def __init__(self, type: str) -> None:
        super().__init__(type)

        data: dict = self.getData()

        self.warriorType: str = data["warrior"]
        self.spawnAmount: int = data["spawnAmount"]
        self.spawnInterval: float = data["spawnInterval"]

        self.timer: Timer = Timer(self.spawnInterval)

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player) -> None:
        """ Updates spawner and spawns warriors """
        super().update(window, camOffset, tileset, player)

        if super().isPlacing():
            return

        self.timer.update(window)

        # If the timer has been activated
        # (or more than once in the past frame, if lag)
        while self.timer.completed():
            for _ in range(self.spawnAmount):
                # Queue the warrior type to be spawned
                DungeonScene.queuedAllies.append(
                    Warrior(self.warriorType, super().getLevel(), True)
                )
