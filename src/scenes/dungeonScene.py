import logging
from src.scenes.baseScene import BaseScene
from src.window import Window
from src.entities.warrior import Warrior
from src.entities.projectile import Projectile
from src.utility.image import Image
from src.tileset import Tileset
from src.waves import Waves


class DungeonScene(BaseScene):
    """ Inherits from BaseScene
        Manages a scene that has warriors """
    log = logging.getLogger(__name__)

    # Append to this list to queue allies to spawn
    queuedAllies: list[Warrior] = []

    def __init__(self, mapFolderName: str) -> None:
        super().__init__(mapFolderName)

        self.enemies: list[Warrior] = []
        self.allies: list[Warrior] = []

        # Projectiles fired by warriors
        self.projectiles: list[Projectile] = []

        # List of tile coords where enemies can spawn,
        # and where allies can spawn from data/maps/dungeon/data.json
        tileset = super().getTileset()
        enemySpawns = tileset.getData()["enemySpawns"]
        allySpawns = tileset.getData()["allySpawns"]
        Warrior.setSpawnPositions(allySpawns, enemySpawns)

        self.waves = Waves()

    def update(self, window: Window) -> None:
        """ Updates warriors, spawns enemies,
            and updates projectiles"""
        super().update(window)

        self.updateWarriors(window)
        self.spawnQueue()

        self.updateProjectiles(window)

        self.waves.update(window)

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

        # Remove dead warriors through list comprehension in place
        self.allies[:] = [ally for ally in self.allies
                          if not self.warriorDead(ally)]

        self.enemies[:] = [enemy for enemy in self.enemies
                           if not self.warriorDead(enemy)]

    def warriorDead(self, warrior: Warrior) -> bool:
        """ Returns True if the warrior is dead.
            Also adds death particles to the scene """
        if warrior.isDead():
            # Add death particles
            deathParticles = warrior.getDeathParticles()
            super().addParticles(deathParticles)

            return True

        return False

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
            projectile.collisions(warriorsList)

        # Only keep projectiles that are in the bounds
        self.projectiles[:] = [  # list comprehension in place
            projectile for projectile in self.projectiles
            if not projectile.shouldRemove()
        ]

    def spawnQueue(self) -> None:
        """ Spawns queued warrior types """
        # Iterate through spawn queue and add them to the correct list
        for warrior in self.queuedAllies:
            self.allies.append(warrior)
        self.queuedAllies.clear()

        for warrior in self.waves.getSpawnQueue():
            self.enemies.append(warrior)
        self.waves.clearSpawnQueue()

    def render(self, surface: Window | Image) -> None:
        """ Renders tileset, warriors, player, and projectiles """
        super().renderTileset(surface)
        self.renderWarriors(surface)
        super().renderPlayer(surface)
        self.renderProjectiles(surface)
        super().renderParticles(surface)

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
