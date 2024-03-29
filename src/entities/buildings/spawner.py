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
        self.spawnInfo: dict = {}

        self.timer: Timer = Timer(0)
        self.unlockedWarriors: list[str] = []

        super().__init__(type)

    def onUpgrade(self, levelData: dict) -> None:
        """ Loads the new unlocked warrior spawning info """
        # Putting the warrior spawn info into the dict
        warriorType = levelData["unlockedWarrior"]
        self.spawnInfo[warriorType] = {
            "spawnAmount": levelData["spawnAmount"],
            "spawnInterval": levelData["spawnInterval"]
        }
        self.unlockedWarriors.append(warriorType)

        # Sets the warrior to spawn to the newly unlocked warrior
        self.chooseWarrior(warriorType)

    def chooseWarrior(self, spawnType: str) -> None:
        """ Chooses the warrior to spawn """
        self.spawnType: str = spawnType

        # Index of warrior in the list of warrior names
        self.warriorIndex: int = self.unlockedWarriors.index(spawnType)

        self.spawnAmount: int = self.spawnInfo[spawnType]["spawnAmount"]
        self.spawnInterval: float = self.spawnInfo[spawnType]["spawnInterval"]

        self.timer.setDelay(self.spawnInterval)

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player, sfxVol: float) -> None:
        """ Updates spawner and spawns warriors """
        super().update(window, camOffset, tileset, player, sfxVol)

        if super().isPlacing():
            return

        self.timer.update(window)

        # If the timer has been activated
        # (or more than once in the past frame, if lag)
        while self.timer.completed():
            for _ in range(self.spawnAmount):
                # Queue the warrior type to be spawned
                DungeonScene.queuedAllies.append(
                    Warrior(self.spawnType,
                            super().getLevel() - self.warriorIndex,
                            True)
                )

    # Getters
    def getSpawnType(self) -> str:
        """ Returns the type of warrior to spawn """
        return self.spawnType

    def getMaxWarrior(self) -> int:
        """ Returns the index of the highest warrior that can be spawned """
        return super().getLevel() - 1

    def getWarriorIndex(self) -> int: return self.warriorIndex
    def getUnlocked(self) -> list[str]: return self.unlockedWarriors
