import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window
from src.utility.database import Database
import src.utility.utility as util
from src.ui.interfaces.tutorial import Tutorial
from src.utility.image import Image
from src.utility.vector import Vect


class MainMenu(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self, window: Window, database: Database) -> None:
        """ Create/initialize the main menu """
        super().__init__("mainMenu")

        self.db: Database = database
        self.setupDatabase()

        self.open(window)

        self.tutorial: Tutorial = Tutorial()

    def setupDatabase(self) -> None:
        """ Sets up the settings database table """
        self.db.makeTable("settings", "type TEXT, value INTEGER")

        # Load the audio settings
        self.sfxVol = self.db.setIfNone("settings",
                                        "type", "sfx",
                                        "value", 50) / 100

        self.musicVol = self.db.setIfNone("settings",
                                          "type", "music",
                                          "value", 50) / 100

    def open(self, window: Window) -> None:
        """ Opens the main menu """
        super().startTransition("visible", window)

    def update(self, window: Window) -> None:
        """ Updates the menu and the scene behind it """
        super().update(window)

        if self.tutorial.isHidden():
            # Updating the main menu buttons
            self.checkPlayButton(window)
            self.checkTutorialButton(window)
            self.updateSettingsButtons(window)

        self.tutorial.update(window)

    def checkPlayButton(self, window: Window) -> None:
        """ Checks if the play button is pressed """
        if super().getElement("play").getActivated():
            self.startTransition("hidden", window)

    def checkTutorialButton(self, window: Window) -> None:
        if super().getElement("tutorial").getActivated():
            self.tutorial.show(window)

    def updateSettingsButtons(self, window: Window) -> None:
        """ Updates the settings buttons """
        # Get direction to move music volume
        dir: int = super().getElement("musicRight").getHeld() - \
            super().getElement("musicLeft").getHeld()

        # Move the music volume, clamping between 0 and 1
        self.musicVol += dir * 0.75 * window.getDeltaTime()
        self.musicVol = util.clamp(self.musicVol, 0, 1)
        super().getElement("musicText").setText(  # Update displayed %
            f"{round(self.musicVol * 100)}%"
        )

        # Do the same for the sfx volume
        dir: int = super().getElement("sfxRight").getHeld() - \
            super().getElement("sfxLeft").getHeld()

        self.sfxVol += dir * 0.75 * window.getDeltaTime()
        self.sfxVol = util.clamp(self.sfxVol, 0, 1)
        super().getElement("sfxText").setText(
            f"{round(self.sfxVol * 100)}%"
        )

    def render(self, surface: Window | Image, offset: Vect = Vect()) -> None:
        """ Renders the menu """
        super().render(surface, offset)

        self.tutorial.render(surface, offset)

    def saveVolume(self) -> None:
        """ Saves the volume """
        self.db.update("settings",
                       "type", "sfx",
                       "value", self.sfxVol * 100)

        self.db.update("settings",
                       "type", "music",
                       "value", self.musicVol * 100)

    def setWaveHighscore(self, highscore: int) -> None:
        """ Sets the wave highscore """
        super().getElement("waveHighscore").setText(
            f"Highscore: Wave {highscore}"
        )

    def isOpen(self) -> bool: return super().getPosType() == "visible"
    def getSFXVol(self) -> float: return self.sfxVol
    def getMusicVol(self) -> float: return self.musicVol
