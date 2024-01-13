import logging

from src.tileset import Tileset
from src.entities.player import Player
from src.utility.vector import Vect
from src.utility.image import Image
from src.window import Window
from src.particle import Particle
from src.ui.interfaces.errorUI import ErrorUI


class BaseScene:
    """ Handles/contains tileset, player, camera offset,
        and other scene-related things """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: str):
        try:
            cls.CAMERA_SPEED: float = constants["game"]["cameraSpeed"]
        except KeyError:
            ErrorUI.create("Unable to find game -> cameraSpeed in constants",
                           cls.log, recoverable=True)
            cls.CAMERA_SPEED: float = 5

    def __init__(self, mapFolderName: str) -> None:
        """ Sets up tileset, players, and camera offset """
        self.log.info("Initializing scene for map " + mapFolderName)

        self.tileset: Tileset = Tileset(mapFolderName)
        self.player: Player = Player(self.tileset.getPlayerStart())

        self.cameraOffset: Vect = Vect()

        self.particles: list[Particle] = []

    def update(self, window: Window) -> None:
        """ Update scene objects """
        self.updateCameraPos(window)

        self.updatePlayer(window)
        self.updateParticles(window)

    def updateUI(self, window: Window) -> None:
        """ Override in subclasses to update UIs """

    def playSounds(self, play: bool) -> None:
        """ Override in subclasses to start or stop sounds """

    def updatePlayer(self, window: Window) -> None:
        """ Update player """
        self.player.update(window, self.tileset)

    def updateCameraPos(self, window: Window) -> None:
        """ Update camera position """
        winSize = window.getSize()
        tileSize = self.tileset.getSize()

        # Camera position centered on the position
        newOffset = self.player.getCenterPos() - window.getSize() / 2

        if tileSize.x < winSize.x:
            # Center the map offset on the screen if
            # it's smaller than the screen
            newOffset.x = tileSize.x / 2 - winSize.x / 2
        else:
            # Clamp the offset to the map size
            newOffset.clampX(0, tileSize.x - winSize.x)

        if tileSize.y < winSize.y:
            newOffset.y = tileSize.y / 2 - winSize.y / 2
        else:
            newOffset.clampY(0, tileSize.y - winSize.y)

        # Move the camera offset slowly to the new position
        self.cameraOffset += ((newOffset - self.cameraOffset) *
                              self.CAMERA_SPEED * window.getDeltaTime())

    def updateParticles(self, window: Window) -> None:
        """ Update particles """
        for particle in self.particles:
            particle.update(window)

        # Remove particles that are done
        self.particles[:] = [particle for particle in self.particles
                             if not particle.isDone()]

    def render(self, surface: Window | Image) -> None:
        """ Render scene objects """
        self.renderTileset(surface)
        self.renderPlayer(surface)
        self.renderParticles(surface)

    def renderTileset(self, surface: Window | Image) -> None:
        """ Render the tileset """
        self.tileset.render(surface, -self.cameraOffset)

    def renderPlayer(self, surface: Window | Image) -> None:
        """ Render the player """
        self.player.render(surface, -self.cameraOffset)

    def renderParticles(self, surface: Window | Image) -> None:
        """ Render particles """
        for particle in self.particles:
            particle.render(surface, -self.cameraOffset)

    # Getters
    def getCamOffset(self) -> Vect: return self.cameraOffset
    def getPlayer(self) -> Player: return self.player
    def getTileset(self) -> Tileset: return self.tileset
    def getParticles(self) -> list[Particle]: return self.particles

    # Setters
    def addParticles(self, particles: list[Particle]) -> None:
        """ Adds particles to the scene """
        self.particles.extend(particles)
