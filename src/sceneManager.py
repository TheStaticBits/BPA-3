import logging
import enum
from src.scenes.baseScene import BaseScene
from src.scenes.buildingsScene import BuildingsScene
from src.scenes.dungeonScene import DungeonScene
from src.ui.interfaces.resourcesUI import ResourcesUI
from src.ui.interfaces.optionsUI import OptionsUI
from src.window import Window
from src.utility.image import Image
from src.utility.database import Database
from src.ui.interfaces.loseUI import LoseUI
from src.ui.interfaces.mainMenu import MainMenu
from src.entities.player import Player


class SceneState(enum.Enum):
    """ The state of the scene """

    BUILDING = "Base"
    DUNGEON = "Dungeon"


class SceneManager:
    """ Manages any scenes and their interactions,
        including transitions and spawning enemies.
        It also manages any shared UI elements. """
    log = logging.getLogger(__name__)

    def __init__(self, window: Window, database: Database) -> None:
        """ Create the scene objects """

        # Current scene being shown & updated
        self.state = SceneState.BUILDING
        self.otherState = SceneState.DUNGEON

        # Shared UI elements
        # Handling resource numbers and icons in the top left
        self.resourcesUI = ResourcesUI()
        self.optionsUI = OptionsUI()

        self.mainMenu = MainMenu(window, database)
        self.loseUI: LoseUI = LoseUI()

        self.db = database
        self.resetScenes()  # Create scenes

    def resetScenes(self) -> None:
        """ Resets the scenes """
        musicVol: float = self.mainMenu.getMusicVol()

        # Dictionary of all the scenes
        self.scenes: dict[SceneState, BaseScene] = {
            SceneState.BUILDING: BuildingsScene("buildings", musicVol),
            SceneState.DUNGEON: DungeonScene("dungeon", musicVol, self.db)
        }

        Player.resetResources()

    def update(self, window: Window) -> None:
        """ Update the current scene """
        self.loseUI.update(window)
        self.mainMenu.update(window)

        # Main menu open
        if self.mainMenu.isOpen():
            # Update the UI, allowing it to adjust to changes
            # in the window size
            self.updateOnlyUI(window)

        # Lose UI open
        elif self.loseUI.isOpen():
            self.updateOnlyUI(window)

            # Test if the user pressed the lose UI close button
            if self.loseUI.pressedClosed():
                # Reset the entire game
                self.loseUI.reset(window)
                self.resetScenes()
                # Update scenes to make sure they're set up
                self.updateScene(window)

        # No ui open, player is playing
        else:
            # Updating the entire game
            self.updateScene(window)

            # Test if the player has lost, then get wave num and set
            # the lose UI to show
            if self.scenes[SceneState.DUNGEON].hasLost():
                self.lost = True
                waveNum: int = self.scenes[SceneState.DUNGEON].getWaveNum()
                self.loseUI.show(window, waveNum)

            # Test if the player pressed pause
            elif self.optionsUI.pausePressed():
                # Open the main menu
                self.mainMenu.open(window)

    def updateScene(self, window: Window) -> None:
        """ Updates everything necessary for the player to play """
        self.optionsUI.update(window)
        self.scenes[self.state].update(window, self.mainMenu.getSFXVol(),
                                       self.mainMenu.getMusicVol())

        # Update the hidden scene without any inputs or sounds
        window.setHideInputs(True)
        self.scenes[self.otherState].update(window, 0, 0)
        window.setHideInputs(False)

        self.updateResources(window)
        self.testSwitchScene(window)

    def updateOnlyUI(self, window: Window) -> None:
        """ Updates only the UI of the current scene,
            this allows the UI to adjust to changes in the window size
            when there is a foreground UI like the main menu """
        # Preventing mouse interactions with the UI
        window.setHideInputs(True)
        # Updates the current scene, without any inputs
        self.scenes[self.state].update(window, 0, self.mainMenu.getMusicVol())
        self.optionsUI.update(window)
        window.setHideInputs(False)

        self.updateResources(window)

    def updateResources(self, window: Window) -> None:
        """ Update wave number and resource numbers shown """
        waveNum: int = self.scenes[SceneState.DUNGEON].getWaveNum()
        self.resourcesUI.update(window, waveNum)

    def testSwitchScene(self, window: Window) -> None:
        """ Tests if the scene should be switched """
        # Pressed switch scene button or the shift key
        if self.optionsUI.switchScene() or window.getJustPressed("shift"):
            # Update switch scene button's text and switch it
            self.optionsUI.updateSceneText(self.state.value)

            # Switch the scene
            self.state, self.otherState = self.otherState, self.state

    def render(self, surface: Window | Image) -> None:
        """ Render the current scene """
        self.scenes[self.state].render(surface)

        self.resourcesUI.render(surface)
        self.optionsUI.render(surface)

        self.loseUI.render(surface)
        self.mainMenu.render(surface)

    def save(self) -> None:
        """ Saves the game """
        self.mainMenu.saveVolume()
