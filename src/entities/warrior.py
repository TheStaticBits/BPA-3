from __future__ import annotations

import logging
import random
from math import cos, sin
from src.entities.entity import Entity
from src.window import Window
import src.utility.utility as util
from src.tileset import Tileset
from src.utility.vector import Vect
from src.utility.image import Image


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

    def __init__(self, type: str, level: int,
                 spawnPosList: list[list[int]]) -> None:
        """ Setup randomized position, its animation, stats, etc. """
        spawnPos = self.pickSpawnPos(spawnPosList)
        super().__init__(self.WARRIOR_DICT[type]["anim"], pos=spawnPos)

        self.type: str = type
        self.variant = self.WARRIOR_DICT[type]["type"]  # melee, ranged, etc.
        self.level: int = level
        self.setStats(self.level)

        # Enemy to target, move to, and attack
        self.target: Warrior = None

    def pickSpawnPos(self, spawnPosList: list[list[int]]) -> Vect:
        """ Picks a random spawn position from the list """
        spawnPos: list[int] = random.choice(spawnPosList)
        return Vect(spawnPos) * Tileset.TILE_SIZE

    def setStats(self, level: int) -> None:
        """ Sets the warrior's stats based on level """
        data = self.WARRIOR_DICT[self.type]["levels"][level - 1]

        self.health: int = data["health"]
        self.damage: int = data["damage"]
        self.interval: float = data["interval"]
        self.range: float = data["range"] * Image.SCALE
        self.speed: float = data["speed"] * Image.SCALE

    def update(self, window: Window, tileset: Tileset,
               opponents: list[Warrior]) -> None:
        """ Updates warrior: moving, attacking, etc."""
        super().update(window)

        # Update target and then move towards it
        self.updateTarget(opponents)
        self.moveToTarget(window)

        # Lock to tileset
        super().lockToRect(Vect(0, 0), tileset.getSize())

    def updateTarget(self, opponents: list[Warrior]) -> None:
        """ Finds the closest opponent to target """
        if len(opponents) == 0:
            return

        lowestDist: float = super().getPos().dist(opponents[0].getPos())

        for warrior in opponents:
            # Get distance from warrior
            dist = super().getPos().dist(warrior.getPos())
            if dist < lowestDist:
                self.target = warrior
                lowestDist = dist

    def moveToTarget(self, window: Window) -> None:
        """ Finds angle to target and moves to it until it's in range """
        if self.target is None:
            return

        pos: Vect = super().getCenterPos()
        targetPos: Vect = self.target.getCenterPos()

        # Check if in range
        dist: float = pos.dist(targetPos)
        if dist <= self.range:
            return  # don't move any further

        # Create velocity vector from angle to target
        angle: float = pos.angle(targetPos)

        velocity: Vect = Vect()
        velocity.x = -self.speed * cos(angle)
        velocity.y = -self.speed * sin(angle)

        velocity *= window.getDeltaTime()

        # Move towards target
        super().setPos(super().getPos() + velocity)

    def hasTarget(self) -> bool:
        """ Returns whether or not the warrior has a target """
        return self.target is not None
