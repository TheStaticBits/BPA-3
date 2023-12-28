import logging
from src.scenes.baseScene import BaseScene
from src.window import Window
from src.entities.warrior import Warrior
from src.entities.projectile import Projectile
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

        # Projectiles fired by warriors
        self.projectiles: list[Projectile] = []

        # List of tile coords where enemies can spawn,
        # and where allies can spawn from data/maps/dungeon/data.json
        self.enemySpawns: list[list[int]] = \
            super().getTileset().getData()["enemySpawns"]

        self.allySpawns: list[list[int]] = \
            super().getTileset().getData()["allySpawns"]

        # temp enemy spawner (remove when waves are added)
        self.timer = Timer(1)

    def update(self, window: Window) -> None:
        super().update(window)

        self.updateWarriors(window)
        self.spawnQueue()

        self.updateProjectiles(window)

        self.timer.update(window)
        while self.timer.completed():
            self.queuedEnemies.append("testWarrior")

    def updateWarriors(self, window: Window) -> None:
        """ Updates warriors (both allies and enemies) """
        tileset: Tileset = super().getTileset()

        # Updating warriors with the opponent list of warriors
        for ally in self.allies:
            ally.update(window, tileset, self.enemies)
            ally.updateAttack(window, self.enemies, self.projectiles)

        for enemy in self.enemies:
            enemy.update(window, tileset, self.allies)
            enemy.updateAttack(window, self.allies, self.projectiles)

    def updateProjectiles(self, window: Window) -> None:
        """ Updates the projectiles, removing those out of bounds """
        tileset = super().getTileset()

        for projectile in self.projectiles:
            projectile.update(window, tileset)

            # Pick the list of warriors to test for
            # collisions on based on the projectile data
            if projectile.hitsEnemies():
                warriorsList = self.enemies
            else:
                warriorsList = self.allies

            # Test for hits
            warriorHit: Warrior = projectile.collisions(warriorsList)

            # If dead remove from the list
            if warriorHit is not None and warriorHit.isDead():
                warriorsList.remove(warriorHit)

        # Only keep projectiles that are in the bounds
        self.projectiles = [  # list comprehension
            projectile for projectile in self.projectiles
            if not projectile.shouldRemove()
        ]

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
        """ Renders tileset, warriors, player, and projectiles """
        super().renderTileset(surface)
        self.renderWarriors(surface)
        super().renderPlayer(surface)
        self.renderProjectiles(surface)

    def renderWarriors(self, surface: Window | Image) -> None:
        """ Renders all warriors """
        for ally in self.allies:
            ally.render(surface, -super().getCamOffset())

        for enemy in self.enemies:
            enemy.render(surface, -super().getCamOffset())

    def renderProjectiles(self, surface: Window | Image) -> None:
        """ Renders projectiles """
        for projectile in self.projectiles:
            projectile.render(surface, -super().getCamOffset())
