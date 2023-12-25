from __future__ import annotations

import random
import logging
from src.entities.entity import Entity
from src.window import Window
import src.utility.utility as util


class Warrior(Entity):
    """ Handles warrior functionality,
        including movement and pathfinding """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the warrior data JSON file """
        cls.WARRIOR_DICT: str = util.loadJSON(
            constants["warriors"]["jsonPath"]
        )

    def __init__(self, type: str) -> None:
        """ Setup position, animation, etc. """
        super().__init__(self.WARRIOR_DICT[type]["anim"])

        self.target = None

    def update(self, window: Window, opponents: list[Warrior]) -> None:
        super().update(window)

        if self.target is None:
            self.findTarget(opponents)

    def findTarget(self, opponents: list[Warrior]) -> None:
        """ Finds the closest opponent to attack
            that is not already a target """
        if len(opponents) == 0:
            return

        lowestDist: float = super().getPos().dist(opponents[0].getPos())

        for warrior in opponents:
            # Find closets enemy not targeted by another warrior
            if warrior.hasTarget():
                continue

            # Get distance from warrior
            dist = super().getPos().dist(warrior.getPos())
            if dist < lowestDist:
                self.target = warrior
                lowestDist = dist

        # All enemies have a target already, so pick a random one
        if self.target is None:
            self.target = random.choice(opponents)

    def hasTarget(self) -> bool:
        """ Returns whether or not the warrior has a target """
        return self.target is not None
