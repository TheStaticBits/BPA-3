from __future__ import annotations

import logging
import random
from src.entities.entity import Entity
from src.entities.projectile import Projectile
from src.window import Window
import src.utility.utility as util
from src.tileset import Tileset
from src.utility.vector import Vect
from src.utility.image import Image
from src.utility.timer import Timer
from src.utility.animation import Animation
from src.particle import Particle
from src.ui.interfaces.errorUI import ErrorUI


class Warrior(Entity):
    """ Handles warrior functionality,
        including movement and pathfinding """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the warrior data JSON file """
        try:
            cls.WARRIOR_DICT: str = util.loadJSON(
                constants["warriors"]["jsonPath"]
            )
        except KeyError:
            ErrorUI.create("Unable to find warriors -> jsonPath in constants",
                           cls.log)

        try:
            cls.KNOCKBACK_ANGLE_RANGE: float = \
                constants["warriors"]["knockbackAngleRange"]
        except KeyError:
            ErrorUI.create("Unable to find warriors -> knockbackAngleRange "
                           "in constants, defaulting to 1", cls.log,
                           recoverable=True)
            cls.KNOCKBACK_ANGLE_RANGE: float = 1

        try:
            # Damage flash of red
            cls.DAMAGE_TINT: tuple[int] = constants["warriors"]["damageTint"]
            cls.DAMAGE_TIME: float = constants["warriors"]["damageTime"]
        except KeyError:
            ErrorUI.create("Unable to find warriors -> [damageTint or "
                           "damageTime] in constants", cls.log,
                           recoverable=True)
            cls.DAMAGE_TINT: tuple[int] = (255, 100, 100)
            cls.DAMAGE_TIME: float = 0.2

        try:
            # Death particles
            particles = constants["warriors"]["deathParticles"]
            cls.PARTICLE_AMOUNT: int = particles["amount"]
            cls.PARTICLE_SIZE: Vect = Vect(particles["size"]) * Image.SCALE
            cls.PARTICLE_SPEED: float = particles["speed"]
            cls.PARTICLE_DURATION: float = particles["duration"]
        except KeyError:
            ErrorUI.create("Unable to find warriors -> deathParticles -> "
                           "[amount, size, speed, or duration] in constants",
                           cls.log)

    @classmethod
    def setSpawnPositions(cls, allySpawns: list[list[int]],
                          enemySpawns: list[list[int]]) -> None:
        cls.ALLY_SPAWNS: list[list[int]] = allySpawns
        cls.ENEMY_SPAWNS: list[list[int]] = enemySpawns

    def __init__(self, type: str, level: int, isAlly: bool) -> None:
        """ Setup randomized position, its animation, stats, etc. """
        spawnPos = self.pickSpawnPos(isAlly)

        # Get the animation data based on whether it's an ally or enemy
        # as allies and enemies have different images
        self.isAlly = isAlly
        if isAlly:
            animData = self.WARRIOR_DICT[type]["allyAnim"]
        else:
            animData = self.WARRIOR_DICT[type]["enemyAnim"]

        # Load the animation and pos
        super().__init__(animData, pos=spawnPos)

        self.type: str = type  # type of warrior in warriors.json (the key)
        # projectile, or aoe:
        self.attackType = self.WARRIOR_DICT[type]["attackType"]
        self.setStats(level)

        # Load warrior-type specific data
        if self.attackType == "projectile":
            # Load the spawn offset for projectiles from the warrior's pos
            self.projectileSpawnPos = Vect(
                self.WARRIOR_DICT[type]["projectileSpawnPos"]
            ) * Image.SCALE

        elif self.attackType == "aoe":
            # Load the aoe animation
            data = self.WARRIOR_DICT[type]["aoeAttackAnim"]
            self.aoeAnim = Animation(data["path"],
                                     data["frames"],
                                     data["delay"],
                                     oneTime=True)

            self.aoeAnim.setToEnd()  # So it doesn't play immediately
            self.aoeAnimPos: Vect = Vect()  # Position of the aoe attack

        self.speed = 0
        self.angle = 0

        # Knockback of projectiles and other such attacks
        self.knockbackAngle = 0
        self.knockbackVel = 0

        # Enemy to target, move to, and attack
        self.target: Warrior = None

        # Damage flash indicator
        self.damageTimer: Timer = Timer(self.DAMAGE_TIME)
        self.showDamageTint: bool = False

    def pickSpawnPos(self, isAlly: bool) -> Vect:
        """ Picks a random spawn position
            from the appropriate spawn positions list """
        spawnList = self.ALLY_SPAWNS if isAlly else self.ENEMY_SPAWNS

        # Choose a random spawn position from the list
        spawnPos: list[int] = random.choice(spawnList)
        return Vect(spawnPos) * Tileset.TILE_SIZE

    def setStats(self, level: int) -> None:
        """ Sets the warrior's stats based on level """
        self.level = level
        data = self.WARRIOR_DICT[self.type]["levels"][level - 1]

        self.health: int = data["health"]
        self.damage: int = data["damage"]
        self.attackTimer: Timer = Timer(data["attackInterval"])
        self.range: float = data["range"] * Image.SCALE

        self.maxSpeed: float = data["maxSpeed"] * Image.SCALE
        self.accel: float = data["accel"] * Image.SCALE
        self.decel: float = data["decel"] * Image.SCALE

        self.knockbackResistance = data["knockbackResistance"] * Image.SCALE
        self.attackKnockback: float = data["attackKnockback"] * Image.SCALE

        if self.attackType == "projectile":
            self.projectileSpeed: float = data["projectileSpeed"] * Image.SCALE

    def update(self, window: Window, tileset: Tileset,
               opponents: list[Warrior]) -> None:
        """ Updates warrior: moving, attacking, etc."""
        super().update(window)

        # Update target and then move towards it
        self.updateTarget(opponents)
        self.updateSpeed(window)
        self.moveToTarget(window)
        self.updateKnockback(window)

        # Lock to tileset
        super().lockToRect(Vect(0, 0), tileset.getSize())

        if self.attackType == "aoe":
            self.updateAoeAttack(window)

        # Update damage tint timer
        if self.showDamageTint:
            self.damageTimer.update(window)
            if self.damageTimer.completed():
                self.showDamageTint = False
                self.damageTimer.reset()

    def updateTarget(self, opponents: list[Warrior]) -> None:
        """ Finds the closest opponent to target
            if the warrior does not already have a target """
        if self.hasTarget() and self.target.isDead():
            self.target = None  # Reset target if it's dead

        if self.hasTarget() or len(opponents) == 0:
            return

        self.target = opponents[0]
        lowestDist: float = super().getPos().dist(opponents[0].getPos())

        for warrior in opponents:
            # Get distance from warrior
            dist = super().getPos().dist(warrior.getPos())
            if dist < lowestDist:
                self.target = warrior
                lowestDist = dist

        # Reset attack timer
        self.attackTimer.reset()

    def updateSpeed(self, window: Window) -> None:
        """ Updates the warrior's speed based on whether
            they're in range and/or have a target """
        if not self.hasTarget():
            self.speed = self.decelerate(window, self.speed, self.decel)
            return

        pos: Vect = super().getCenterPos()
        targetPos: Vect = self.target.getCenterPos()

        # Check if in range
        dist: float = pos.dist(targetPos)
        if dist <= self.range:  # In range, so decelerate
            self.speed = self.decelerate(window, self.speed, self.decel)
        else:  # Not in range, so accelerate
            self.speed = self.accelerate(window, self.speed, self.accel)

    def moveToTarget(self, window: Window) -> None:
        """ Finds angle to target and moves to it until it's in range """
        if self.hasTarget():  # If there's a target, update the angle
            pos: Vect = super().getCenterPos()
            targetPos: Vect = self.target.getCenterPos()

            # Gets the angle from this warrior to the target
            self.angle: float = pos.angle(targetPos)

        if self.speed <= 0:
            return

        # Find velocity based on angle and speed
        velocity: Vect = Vect.angleMove(self.angle) * \
            self.speed * window.getDeltaTime()

        # add movement amount
        super().addPos(velocity)

    def updateKnockback(self, window: Window) -> None:
        """ Updates the knockback, decelerating it and moving by it """
        if self.knockbackVel <= 0:
            return

        # Decelerate knockback
        self.knockbackVel = self.decelerate(window,
                                            self.knockbackVel,
                                            self.knockbackResistance)

        # Get velocity from angle and speed
        velocity: Vect = Vect.angleMove(self.knockbackAngle) * \
            self.knockbackVel * window.getDeltaTime()

        # Add movement amount
        super().addPos(velocity)

    def decelerate(self, window: Window,
                   velocity: float, decel: float) -> float:
        """ Decelerates vel to 0 and returns the new velocity"""
        if velocity > 0:
            velocity -= decel * window.getDeltaTime()
            if velocity < 0:
                velocity = 0

        return velocity

    def accelerate(self, window: Window,
                   velocity: float, accel: float) -> float:
        """ Accelerates velocity to self.maxSpeed and returns it """
        if velocity < self.maxSpeed:
            velocity += accel * window.getDeltaTime()
            if velocity > self.maxSpeed:
                velocity = self.maxSpeed

        return velocity

    def updateAttack(self, window: Window, opponents: list[Warrior],
                     projectiles: list[Projectile]) -> None:
        """ Updates the warrior's attack, and attacking when timer is up """
        if not self.hasTarget() or self.speed > 0:
            return

        # Update attack timer
        self.attackTimer.update(window)

        while self.attackTimer.completed():
            self.attack(opponents, projectiles)

    def attack(self, opponents: list[Warrior],
               projectiles: list[Projectile]) -> None:
        """ Attacks, based on self.attackType """
        if self.attackType == "projectile":
            self.spawnProjectile(projectiles)

        elif self.attackType == "aoe":
            self.aoeAttack(opponents)

    def spawnProjectile(self, projectiles: list[Projectile]) -> None:
        """ Spawns a projectile from warrior data """
        # position of warrior plus projectile spawn offset
        spawnPos: Vect = super().getPos() + self.projectileSpawnPos
        # angle from the particle spawn position to the target
        angle = spawnPos.angle(self.target.getCenterPos())

        # Create projectile object from data
        proj: Projectile = Projectile(self.type, angle,
                                      self.projectileSpeed, self.damage,
                                      self.attackKnockback,
                                      spawnPos, self.isAlly)

        projectiles.append(proj)

    def aoeAttack(self, opponents: list[Warrior]) -> None:
        """ Deals damage to all opponents in range """
        self.aoeAnim.restart()  # Sets the attack anim to play
        # Center aoe attack animation on the player
        self.aoeAnimPos = super().getCenterPos() - self.aoeAnim.getSize() / 2

        # Create circle image to test for pixel-perfect collisions
        # with all opponents in range
        circle = Image.makeEmpty(Vect(self.range * 2), False, True)
        circle.drawCircle(self.range, (0, 0, 0))

        # Top left of circle image position
        circlePos: Vect = super().getCenterPos() - self.range

        # Deal damage with pixel perfect collision to all opponents in range
        for opponent in opponents:
            image = opponent.getAnim().getFrame()

            # Test for pixel perfect collision
            collided: bool = circle.pixelPerfectCollide(circlePos, image,
                                                        opponent.getPos())

            if collided:  # Deal damage if collided
                # Getting angle from the center of this warrior to the opponent
                angle = self.getCenterPos().angle(opponent.getCenterPos())

                opponent.hit(self.damage, angle, self.attackKnockback)

    def updateAoeAttack(self, window: Window) -> None:
        """ Updates the aoe attack animation """
        if self.attackType == "aoe":
            self.aoeAnim.update(window)

    def renderAoeAttack(self, surface: Window | Image,
                        offset: Vect = Vect()) -> None:
        """ Renders the aoe attack animation """
        if self.attackType == "aoe":
            if not self.aoeAnim.isFinished():
                self.aoeAnim.render(surface, self.aoeAnimPos + offset)

    def hit(self, damage: float, knockbackAngle: float,
            knockbackVel: float) -> None:
        """ Deals damage to the warrior """
        self.health -= damage

        # Creates a new knockback angle in the random range
        knockbackAngle -= self.KNOCKBACK_ANGLE_RANGE / 2
        knockbackAngle += random.random() * self.KNOCKBACK_ANGLE_RANGE

        self.knockbackAngle = knockbackAngle
        self.knockbackVel = knockbackVel

        self.showDamageTint = True

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the warrior and its aoe attack if necessary """
        self.renderAoeAttack(surface, offset)

        if self.showDamageTint:
            # Render with damage tint
            img = super().getAnim().getFrame().copy()
            img.tint(self.DAMAGE_TINT)
            surface.render(img, super().getPos() + offset)

        else:
            super().render(surface, offset)

    def getDeathParticles(self) -> list[Particle]:
        """ Returns a list of particles for the warrior's death """
        return Particle.generate(self.PARTICLE_AMOUNT,
                                 super().getAnim().getFrame(),
                                 super().getPos(),
                                 self.PARTICLE_SIZE, self.PARTICLE_SPEED,
                                 self.PARTICLE_DURATION)

    # Getters
    def hasTarget(self) -> bool:
        """ Returns whether or not the warrior has a target """
        return self.target is not None

    def isDead(self) -> bool:
        """ Returns whether or not the warrior is dead """
        return self.health <= 0
