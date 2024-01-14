import logging
import pygame
import src.utility.utility as util
from src.entities.entity import Entity
from src.utility.vector import Vect
from src.tileset import Tileset
from src.window import Window
from src.entities.player import Player
from src.utility.image import Image
from src.particle import Particle
from src.ui.interfaces.errorUI import ErrorUI


class BaseBuilding(Entity):
    """ All buildings inherit from this base building class
        Handles placing of buildings, size/hitboxes, etc.
        Inherits from Entity class for animation and position handling. """
    log = logging.getLogger(__name__)

    # Static functions
    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the buildings data JSON file """
        try:
            # Building JSON data file (data/buildings.json)
            cls.BUILDINGS_DATA: dict = util.loadJSON(
                constants["buildings"]["jsonPath"]
            )
        except KeyError:
            ErrorUI.create("Unable to find buildings -> jsonPath in constants",
                           cls.log)

        try:
            # Range in pixels that the player can place buildings
            cls.BUILD_REACH: int = constants["buildings"]["buildReachTiles"] \
                * Tileset.TILE_SIZE.x
        except KeyError:
            ErrorUI.create("Unable to find buildings -> buildReachTiles "
                           "in constants. Defaulting to 5 tiles", cls.log,
                           recoverable=True)
            cls.BUILD_REACH: int = 5 * Tileset.TILE_SIZE.x

        try:
            cls.redTint: tuple[int] = constants["buildings"]["redTint"]
            cls.whiteTint: tuple[int] = constants["buildings"]["whiteTint"]
        except KeyError:
            ErrorUI.create("Unable to find buildings -> [redTint or whiteTint]"
                           " in constants", cls.log, recoverable=True)
            cls.redTint: tuple[int] = (255, 0, 0)
            cls.whiteTint: tuple[int] = (255, 255, 255)

        # Particles
        try:
            particles: dict = constants["buildings"]["effectParticles"]
            cls.PARTICLE_AMOUNT: int = particles["amount"]
            cls.PARTICLE_SIZE: Vect = Vect(particles["size"]) * Image.SCALE
            cls.PARTICLE_SPEED: float = particles["speed"]
            cls.PARTICLE_DURATION: float = particles["duration"]
        except KeyError:
            ErrorUI.create("Unable to find buildings -> effectParticles -> "
                           "[amount, size, speed, or duration] in constants",
                           cls.log)

    @classmethod
    def testPlacement(cls, type: str, tilePos: Vect, tileset: Tileset) -> bool:
        """ Tests if the tiles in the tileset
            at tilePos are occupied or not """
        data: dict = cls.BUILDINGS_DATA[type]

        buildingTileSize = Vect(data["size"])

        # Test if out of range of tiles
        if (tilePos.x + buildingTileSize.x > tileset.getTileSize().x or
                tilePos.y + buildingTileSize.y > tileset.getTileSize().y or
                tilePos.x < 0 or tilePos.y < 0):
            return False

        # Test if any tiles are occupied
        return not tileset.testRangeOccupied(tilePos, buildingTileSize)

    def __init__(self, type: str, level: int = 1) -> None:
        """ Setup initial position, animation, and
            set tiles where the building is to occupied """

        self.type: str = type
        self.placing: bool = True
        self.placable: bool = False
        self.level: int = level
        self.sold: bool = False

        try:
            self.buildingTileSize: Vect = Vect(self.getData()["size"])
        except KeyError:
            ErrorUI.create("Unable to find building -> size in buildings.json"
                           f" for building {self.type}",
                           self.log)

        # Set to True to spawn effect particles
        self.spawnParticles: bool = False

        self.loadLevel(level)  # Load level data

        # Whether the player has selected this building
        # and its upgrades UI is showing.
        # Resets to False every frame
        self.selected: bool = False

        try:
            super().__init__(self.getData()["anim"], Tileset.TILE_SIZE)
        except KeyError:
            ErrorUI.create("Unable to find building -> anim in buildings.json"
                           f" for building {self.type}",
                           self.log)

        # Making sure "levels" is in the building data
        if "levels" not in self.getData():
            ErrorUI.create("Can't find building -> levels in buildings.json"
                           f" for building {self.type}",
                           self.log)

        # Get sound data
        if "sound" in self.getData():
            self.sound: pygame.mixer.Sound = pygame.mixer.Sound(
                self.getData()["sound"]
            )
        else:
            self.sound: pygame.mixer.Sound = None

    def onRemove(self) -> None:
        """ Overriden in subclasses.
            Called on building removal. """

    def onPlace(self) -> None:
        """ Overriden in subclasses.
            Called on building placement. """

    def onUpgrade(self, levelData: dict) -> None:
        """ Overriden in subclasses.
            Called on building upgrade. """

    def loadLevel(self, level: int = None) -> None:
        """ Loads the the level or the next level if level is None """
        if level is None:
            level = self.level + 1

        self.level = level

        # Call load level on subclasses
        self.onUpgrade(self.getLevelData())

    def update(self, window: Window, camOffset: Vect,
               tileset: Tileset, player: Player, sfxVol: float) -> None:
        """ Updates the building by following the cursor and testing placement
            and updating animation if not placing"""
        if self.placing:
            self.followCursor(window, camOffset, tileset, player)
            self.testPlace(window, tileset, player)
        else:  # update animation:
            super().update(window)
            self.updateSound(player, sfxVol)

    def followCursor(self, window: Window, camOffset: Vect,
                     tileset: Tileset, player: Player) -> None:
        """ Moves to cursor and tests if the building can be placed
            Also limits the cursor position to a range around the player """
        # Get cursor position and convert to position on the tileset
        mousePos: Vect = window.getMousePos() + camOffset

        # Get player center position
        playerPos: Vect = player.getCenterPos()

        # Find distance between player and cursor
        dist: Vect = mousePos.dist(playerPos)

        if dist > self.BUILD_REACH:
            # Cursor is too far from player, clamp to max distance

            # Get angle between player and cursor
            angle: float = playerPos.angle(mousePos)

            # Get distance from angle and max distance
            dist: Vect = Vect.angleMove(angle) * self.BUILD_REACH

            # Set mousePos to the new position
            mousePos = playerPos + dist

        # Offset by half the building size
        mousePos -= super().getSize() / 2

        # Calculate tile position of the cursor
        self.tilePos = mousePos / Tileset.TILE_SIZE
        self.tilePos = self.tilePos.floor()

        # Clamp to the tile map so it doesn't go over the edge
        self.tilePos.clamp(Vect(0, 0), tileset.getTileSize() - Vect(1, 1))

        # Set position to new self.tilePos
        super().setPos(self.tilePos * Tileset.TILE_SIZE)

    def testPlace(self, window: Window, tileset: Tileset,
                  player: Player) -> None:
        """ Tests if the building can be placed and places it """
        self.placable = self.testPlacement(self.type, self.tilePos, tileset) \
            and not super().collide(player)

        if self.placable and window.getMouseJustPressed("left"):
            # Placed down the building!
            self.placing = False

            # Sets the range of tiles that the building takes up to occupied
            # so no other building can be placed there
            tileset.setRangeOccupied(self.tilePos, self.buildingTileSize)

            self.sound.play(-1)
            self.setSpawnParticles()
            self.onPlace()

    def updateSound(self, player: Player, sfxVol: float) -> None:
        """ Plays the sound if the player is close enough """
        if self.sound is None:
            return

        volume: float = player.getSoundVolume(super().getCenterPos())
        volume *= sfxVol
        self.sound.set_volume(volume)

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Render with tints if placing """
        if not self.placing and not self.selected:
            super().render(surface, offset)
            return

        # Get current animation frame
        img = super().getAnim().getFrame().copy()

        if self.placing:  # Set semitransparent
            img.setAlpha(150)

            # Tint red if not placeable
            if not self.placable:
                img.tint(*self.redTint)

        elif self.selected:
            # Tint for selected
            img.tint(*self.whiteTint, blendMode=pygame.BLEND_ADD)
            self.selected = False  # Reset selected

        # Draw the new tinted surface to the screen
        surface.render(img, super().getPos() + offset)

    def setSold(self, tileset: Tileset) -> None:
        """ Sets the building to sold and unoccupied """
        self.sold = True

        # Set tiles to be unoccupied:
        tileset.setRangeOccupied(self.tilePos, self.buildingTileSize, False)
        self.onRemove()

        if self.sound is not None:
            self.sound.stop()

    def getParticles(self) -> list[Particle]:
        """ Gets a list of particles used for various situations """
        return Particle.generate(self.PARTICLE_AMOUNT,
                                 super().getAnim().getFrame(),
                                 super().getPos(),
                                 self.PARTICLE_SIZE, self.PARTICLE_SPEED,
                                 self.PARTICLE_DURATION)

    # Getters
    def getData(self) -> dict:
        return self.BUILDINGS_DATA[self.type]

    def getLevelData(self) -> dict:
        """ Returns the level data for the current level """
        return self.getData()["levels"][self.level - 1]

    def getNextLevelData(self) -> dict:
        """ Returns the level data for the next level """
        return self.getData()["levels"][self.level]

    def reachedMaxLevel(self) -> bool:
        """ Returns True if the building has reached the max level """
        return self.level >= len(self.getData()["levels"])

    def isSpawningParticles(self) -> bool:
        """ Returns True if the building is spawning particles
            Also sets the spawnParticles to False """
        if self.spawnParticles:
            self.spawnParticles = False
            return True
        return False

    def isPlacing(self) -> bool: return self.placing
    def getLevel(self) -> int: return self.level
    def isSold(self) -> bool: return self.sold

    @classmethod
    def getDataFrom(cls, type: str) -> dict:
        return cls.BUILDINGS_DATA[type]

    # Setters
    def select(self) -> None: self.selected = True
    def setSpawnParticles(self) -> None: self.spawnParticles = True
