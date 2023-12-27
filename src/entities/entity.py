from __future__ import annotations
import pygame
import logging

from src.utility.animation import Animation
from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window


class Entity:
    """ Base class for all entities in the game.
        Handles the animation and position """
    log = logging.getLogger(__name__)

    def __init__(self, animData: dict, pos: Vect = Vect()) -> None:
        """ Setup base values.
            animData must contain "path", "frames", and "delay" keys.
            pos is an optional argument which is set to (0, 0) by default """
        self.pos: Vect = pos

        self.animation = self.loadAnim(animData)

    @classmethod
    def loadAnim(cls, animData: dict) -> Animation:
        """ Loads the animation object """
        return Animation(animData["path"],
                         animData["frames"],
                         animData["delay"])

    def update(self, window: Window) -> None:
        """ Updates the animation """
        self.animation.update(window)

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the animation at the entity's current position"""
        self.animation.render(surface, self.pos + offset)

    def collision(self, window: Window,
                  entities: list[Entity], velocity: Vect) -> None:
        """ Handle collision with other entities,
            and also updating position based on velocity """

        # Apply velocity in each direction separately
        # and then check for collisions,
        # then adjust pos accordingly to edge of any collisions
        self.pos.x += velocity.x * window.getDeltaTime()
        self.axisCollision("x", velocity, entities)

        self.pos.y += velocity.y * window.getDeltaTime()
        self.axisCollision("y", velocity, entities)

    def axisCollision(self, dir: str, velocity: Vect,
                      entities: list[Entity]) -> None:
        """ Check and adjust pos for any collisions in a single direction.
            dir parameter must be "x" or "y". """

        # Check collision with each entity
        for entity in entities:
            # Collided with an entity
            if self.collide(entity):
                # Get entity position in the direction of collision
                entityStart: float = entity.getPos().get(dir)

                # Collided with top or left
                if velocity.get(dir) > 0:
                    # Set position to the edge of the entity
                    newPos: float = entityStart - self.getSize().get(dir)

                # Collided with bottom or right of entity
                else:
                    # Set pos to bottom or right edge of entity
                    newPos: float = entityStart + entity.getSize().get(dir)

                self.pos.set(dir, newPos)  # Set new position
                velocity.set(dir, 0)  # Reset velocity in that dir

    def collide(self, entity: Entity) -> bool:
        """ Collision detection between an entity and another """
        return self.getRect().colliderect(entity.getRect())

    def lockToRect(self, topLeft: Vect, bottomRight: Vect,
                   velocity: Vect = None) -> None:
        """ Locks the entity to a rect (used for map boundaries) """
        # Clamp position to inside the rect
        bottomRight -= self.getSize()
        self.pos.clamp(topLeft, bottomRight)

        if velocity is None:
            return

        # Reset velocity if the entity is at the edge of the rect
        if self.pos.x == topLeft.x or self.pos.x == bottomRight.x:
            velocity.x = 0

        if self.pos.y == topLeft.y or self.pos.y == bottomRight.y:
            velocity.y = 0

    # Getters
    def getAnim(self) -> Animation: return self.animation
    def getSize(self) -> Vect: return self.animation.getSize()
    def getPos(self) -> Vect: return self.pos

    def getRect(self) -> pygame.Rect:
        return Vect.toRect(self.pos, self.animation.getSize())

    def getCenterPos(self) -> Vect:
        """ Returns the center of the entity """
        return self.pos + (self.animation.getSize() / 2)

    # Setters
    def setPos(self, pos: Vect) -> None: self.pos = pos

    def addPos(self, addPos: Vect) -> None:
        self.pos += addPos
