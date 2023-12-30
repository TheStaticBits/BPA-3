import logging
from math import cos, sin
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.window import Window
from src.tileset import Tileset


class Projectile(Entity):
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the projectile animation data from consts """
        cls.ANIMS: dict = constants["projectiles"]

    def __init__(self, type: str, angle: float, speed: float,
                 damage: float, knockback: float,
                 startingPos: Vect, isAlly: bool) -> None:
        """ Sets up the projectile anim and pos """
        super().__init__(self.ANIMS[type], startingPos)

        self.angle: float = angle
        self.speed: float = speed
        self.damage: float = damage
        self.knockback: float = knockback
        self.isAlly: bool = isAlly

        self.remove: bool = False

        # Center the projectile onto the starting pos
        # by subtracting half its size from the pos
        super().addPos(-super().getSize() // 2)

    def update(self, window: Window, tileset: Tileset) -> None:
        """ Updates the particle anim and movement """
        super().update(window)

        self.move(window)

        self.testOutOfBounds(tileset.getSize())

    def move(self, window: Window) -> None:
        """ Updates the projectile position """
        # Movement based on the angle and speed
        moveAmount: Vect = Vect(
            self.speed * cos(self.angle),
            self.speed * sin(self.angle)
        ) * window.getDeltaTime()
        super().addPos(moveAmount)

    def testOutOfBounds(self, tilesetSize: Vect) -> bool:
        """ Tests and returns True if the projectile is out of the tileset """
        if self.remove:
            return

        pos = super().getPos()
        size = super().getSize()

        # Testing if the projectile hit an edge of the tileset
        self.remove = (pos.x <= 0 or pos.y <= 0 or
                       pos.x + size.x >= tilesetSize.x or
                       pos.y + size.y >= tilesetSize.y)

    def collisions(self, warriors: list) -> None:
        """ Tests if the projectile collides with the entity """
        for warrior in warriors:
            if super().collide(warrior):
                self.remove = True
                warrior.hit(self.damage, self.angle, self.knockback)
                return

    # Getters
    def shouldRemove(self) -> bool: return self.remove
    def hitsEnemies(self) -> bool: return self.isAlly
