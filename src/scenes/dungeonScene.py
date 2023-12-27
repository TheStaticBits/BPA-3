import logging
from src.scenes.baseScene import BaseScene
from src.window import Window
from src.entities.warrior import Warrior
from src.utility.image import Image
from src.tileset import Tileset
from src.utility.timer import Timer


class DungeonScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has warriors """
    log = logging.getLogger(__name__)

    # Append to these lists to queue spawning warriors
    queuedAllies: list[str] = []
    queuedEnemies: list[str] = []

    def __init__(self, mapFolderName: str) -> None:
        super().__init__(mapFolderName)

        self.enemies: list[Warrior] = []
        self.allies: list[Warrior] = []

        # List of tile coords where enemies can spawn,
        # and where allies can spawn from data/maps/dungeon/data.json
        self.enemySpawns: list[list[int]] = \
            super().getTileset().getData()["enemySpawns"]

        self.allySpawns: list[list[int]] = \
            super().getTileset().getData()["allySpawns"]

        # temp
        self.timer = Timer(1)

    def update(self, window: Window) -> None:
        super().update(window)

        self.updateWarriors(window)
        self.spawnQueue()

        self.timer.update(window)
        while self.timer.completed():
            self.queuedEnemies.append("testWarrior")

    def updateWarriors(self, window: Window) -> None:
        """ Updates warriors (both allies and enemies) """
        tileset: Tileset = super().getTileset()

        # Updating warriors with the opponent list of warriors
        for ally in self.allies:
            ally.update(window, tileset, self.enemies)

        for enemy in self.enemies:
            enemy.update(window, tileset, self.allies)

    def spawnQueue(self) -> None:
        """ Spawns queued warrior types """
        for warriorType in self.queuedAllies:
            self.allies.append(Warrior(warriorType, True,
                                       1, self.allySpawns))
        self.queuedAllies.clear()

        for warriorType in self.queuedEnemies:
            self.enemies.append(Warrior(warriorType, False,
                                        1, self.enemySpawns))
        self.queuedEnemies.clear()

    def render(self, surface: Window | Image) -> None:
        """ Renders scene and warriors """
        super().renderTileset(surface)

        for ally in self.allies:
            ally.render(surface, -super().getCamOffset())

        for enemy in self.enemies:
            enemy.render(surface, -super().getCamOffset())

        super().renderPlayer(surface)
