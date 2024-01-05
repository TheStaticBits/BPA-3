import logging
import enum
from src.scenes.baseScene import BaseScene
from src.scenes.buildingsScene import BuildingsScene
from src.scenes.dungeonScene import DungeonScene
from src.ui.interfaces.resourcesUI import ResourcesUI
from src.ui.interfaces.optionsUI import OptionsUI
from src.window import Window
from src.utility.image import Image


class SceneState(enum.Enum):
    """ The state of the scene """

    BUILDING = "Base"
    DUNGEON = "Dungeon"


class SceneManager:
    """ Manages any scenes and their interactions,
        including transitions and spawning enemies.
        It also manages any shared UI elements. """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create the scene objects """

        # Current scene being shown & updated
        self.state = SceneState.BUILDING
        self.otherState = SceneState.DUNGEON

        # Dictionary of all the scenes
        self.scenes: dict[SceneState, BaseScene] = {
            SceneState.BUILDING: BuildingsScene("testmap"),
            SceneState.DUNGEON: DungeonScene("dungeon")
        }

        # Shared UI elements
        # Handling resource numbers and icons in the top left
        self.resourcesUI = ResourcesUI()
        self.optionsUI = OptionsUI()

    def update(self, window: Window) -> None:
        """ Update the current scene """
        self.optionsUI.update(window)  # Update options buttons

        # Update the current scene
        self.scenes[self.state].update(window)

        # Update the hidden scene without any inputs
        window.setHideInputs(True)
        self.scenes[self.otherState].update(window)
        window.setHideInputs(False)

        # Update wave number and resource numbers shown
        waveNum: int = self.scenes[SceneState.DUNGEON].getWaveNum()
        self.resourcesUI.update(window, waveNum)

        self.testSwitchScene()

    def testSwitchScene(self) -> None:
        """ Tests if the scene should be switched """
        if self.optionsUI.switchScene():  # Pressed button
            # Update switch scene button's text and switch it
            self.optionsUI.updateSceneText(self.state.value)

            # Switch the scene
            self.state, self.otherState = self.otherState, self.state

    def render(self, surface: Window | Image) -> None:
        """ Render the current scene """
        self.scenes[self.state].render(surface)

        self.resourcesUI.render(surface)
        self.optionsUI.render(surface)
