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
        self.speed = 0
        self.angle = 0

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

        self.maxSpeed: float = data["maxSpeed"] * Image.SCALE
        self.accel: float = data["accel"] * Image.SCALE
        self.decel: float = data["decel"] * Image.SCALE

    def update(self, window: Window, tileset: Tileset,
               opponents: list[Warrior]) -> None:
        """ Updates warrior: moving, attacking, etc."""
        super().update(window)

        # Update target and then move towards it
        self.updateTarget(opponents)
        self.updateSpeed(window)
        self.moveToTarget(window)

        # Lock to tileset
        super().lockToRect(Vect(0, 0), tileset.getSize())

    def updateTarget(self, opponents: list[Warrior]) -> None:
        """ Finds the closest opponent to target
            if the warrior does not already have a target """
        if self.target is not None or len(opponents) == 0:
            return

        lowestDist: float = super().getPos().dist(opponents[0].getPos())

        for warrior in opponents:
            # Get distance from warrior
            dist = super().getPos().dist(warrior.getPos())
            if dist < lowestDist:
                self.target = warrior
                lowestDist = dist

    def updateSpeed(self, window: Window) -> None:
        """ Updates the warrior's speed based on whether
            they're in range and/or have a target """
        if self.target is None:
            self.decelerate(window)
            return

        pos: Vect = super().getCenterPos()
        targetPos: Vect = self.target.getCenterPos()

        # Check if in range
        dist: float = pos.dist(targetPos)
        if dist <= self.range:  # In range, so decelerate
            self.decelerate(window)
        else:  # Not in range, so accelerate
            self.accelerate(window)

    def moveToTarget(self, window: Window) -> None:
        """ Finds angle to target and moves to it until it's in range """
        if self.target is not None:
            # Update angle to the target if there is one
            pos: Vect = super().getCenterPos()
            targetPos: Vect = self.target.getCenterPos()

            # Create velocity vector from angle to target
            self.angle: float = pos.angle(targetPos)

        # Find velocity based on angle and speed
        velocity: Vect = Vect()
        velocity.x = -self.speed * cos(self.angle)
        velocity.y = -self.speed * sin(self.angle)

        velocity *= window.getDeltaTime()

        # Move towards target
        super().setPos(super().getPos() + velocity)

    def decelerate(self, window: Window) -> None:
        """ Decelerates self.speed to 0 """
        if self.speed > 0:
            self.speed -= self.decel * window.getDeltaTime()
            if self.speed < 0:
                self.speed = 0

    def accelerate(self, window: Window) -> None:
        """ Accelerates self.speed to self.maxSpeed """
        if self.speed < self.maxSpeed:
            self.speed += self.accel * window.getDeltaTime()
            if self.speed > self.maxSpeed:
                self.speed = self.maxSpeed

    def hasTarget(self) -> bool:
        """ Returns whether or not the warrior has a target """
        return self.target is not None
