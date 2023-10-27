import pygame
import logging

from src.utility.animation import Animation
from src.utility.vector import Vect
from src.window import Window


class Entity:
    """ Base class for all entities in the game.
        Handles the animation and position """

    # Cache for spritesheets so as to reduce loading the same image twice
    # Key: image path - Value: the spritesheet
    spritesheets: dict = {}

    def __init__(self, animData: dict, loggerName: str,
                 pos: Vect = Vect()) -> None:
        """ Setup base values.
            animData must contain "path", "frames", and "delay" keys.
            pos is an optional argument which is set to (0, 0) by default """

        self.log = logging.getLogger(loggerName)

        self.pos: Vect = pos

        self.loadSpritesheet(animData["path"])
        self.animation = self.loadAnim(animData)

    def loadSpritesheet(self, animPath: str) -> None:
        """ Loads spritesheet image at path if it's
            not already in the spritesheets variable """
        if animPath not in self.spritesheets:
            self.log.info(f"Loading animation spritesheet at {animPath}")
            self.spritesheets[animPath] = Window.loadImg(animPath)

    def loadAnim(self, animData: dict) -> Animation:
        """ Loads the animation object """
        return Animation(self.spritesheets[animData["path"]],
                         animData["frames"],
                         animData["delay"])

    def update(self, window: Window) -> None:
        """ Updates the animation """
        self.animation.update(window)

    def render(self, window: Window, offset: Vect = Vect()) -> None:
        """ Renders the animation at the entity's current position"""
        self.animation.render(window, self.pos + offset)

    def collision(self, window: Window,
                  entities: list["Entity"], velocity: Vect) -> None:
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
                      entities: list["Entity"]) -> None:
        """ Check and adjust pos for any collisions in a single direction.
            dir parameter must be "x" or "y". """

        # Check collision with each entity
        entity: Entity  # Set the type of the iterator
        for entity in entities:

            # Collided with an entity
            if self.collide(entity):
                # Get entity position in the direction of collision
                entityStart: float = entity.getPos().get(dir)

                # Collided with top or left
                if velocity.get(dir) > 0:
                    # Get width of self in the direction of collision
                    width: float = self.getAnim().getSize().get(dir)

                    # Set position to the edge of the entity
                    newPos: float = entityStart - width

                # Collided with bottom or right of entity
                else:
                    # Set pos to bottom or right edge of entity
                    newPos: float = entityStart + entity.getSize().get(dir)

                self.pos.set(dir, newPos)  # Set new position
                velocity.set(dir, 0)  # Reset velocity in that dir

    def collide(self, entity: "Entity") -> bool:
        """ Collision detection between an entity and another """
        return self.getRect().colliderect(entity.getRect())

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
