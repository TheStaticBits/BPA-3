import logging
from src.scenes.baseScene import BaseScene
from src.window import Window
from src.entities.warrior import Warrior
from src.utility.image import Image


class DungeonScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has warriors """
    log = logging.getLogger(__name__)

    # Append to this list to queue spawning allies
    queuedAllies: list[str] = []

    def __init__(self, mapFolderName: str) -> None:
        super().__init__(mapFolderName)

        self.enemies: list[Warrior] = []
        self.allies: list[Warrior] = []

        # List of tile coords where enemies can spawn
        self.enemySpawns: list[list[int]] = \
            super().getTileset().getData()["enemySpawns"]

    def update(self, window: Window) -> None:
        super().update(window)

        self.updateWarriors(window)
        self.spawnQueue()

    def updateWarriors(self, window: Window) -> None:
        """ Updates warriors (both allies and enemies) """
        for ally in self.allies:
            ally.update(window, self.enemies)

        for enemy in self.enemies:
            enemy.update(window, self.allies)

    def spawnQueue(self) -> None:
        """ Spawns queued ally warrior types """
        for warriorType in self.queuedAllies:
            self.allies.append(Warrior(warriorType))
        self.queuedAllies.clear()

    def render(self, surface: Window | Image) -> None:
        """ Renders scene and warriors """
        super().render(surface)

        for ally in self.allies:
            ally.render(surface, -super().getCamOffset())

        for enemy in self.enemies:
            enemy.render(surface, -super().getCamOffset())
