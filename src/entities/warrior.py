from __future__ import annotations

from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect
import src.utility.utility as util

import random


class Warrior(Entity):
    """ Handles warrior functionality,
        including movement and pathfinding """

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the warrior data JSON file """
        cls.WARRIOR_DICT: str = util.loadJSON(
            constants["warriors"]["jsonPath"]
        )

    def __init__(self, type: str) -> None:
        """ Setup position, animation, etc. """
        super().__init__(self.WARRIOR_DICT[type]["anim"], __name__,
                         Vect(0, 0))

        self.speedX = random.randint(1, 300)
        self.speedY = random.randint(1, 300)

    def update(self, window: Window, opponents: list[Warrior]) -> None:
        super().update(window)

        # Some kind of pathfinding to enemies
        super().getPos().y += self.speedY * window.getDeltaTime()
        super().getPos().x += self.speedX * window.getDeltaTime()
