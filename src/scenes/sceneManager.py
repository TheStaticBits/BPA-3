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

    BUILDING = "Buildings"
    DUNGEON = "Dungeon"


class SceneManager:
    """ Manages any scenes and their interactions,
        including transitions and spawning enemies.
        It also manages any shared UI elements. """

    def __init__(self):
        """ Create the scene objects """

        # Current scene being shown & updated
        self.state = SceneState.BUILDING

        # Dictionary of all the scenes
        self.scenes: dict[SceneState, BaseScene] = {
            SceneState.BUILDING: BuildingsScene("testmap"),
            SceneState.DUNGEON: DungeonScene("dungeon")
        }

        # Shared UI elements
        # Handling resource numbers and icons in the top left
        self.resourcesUI = ResourcesUI()
        self.optionsUI = OptionsUI()

    def update(self, window: Window):
        """ Update the current scene """

        # Update the current scene
        self.scenes[self.state].update(window)

        # Update UIs
        self.resourcesUI.update(window)
        self.optionsUI.update(window)

        self.testSwitchScene()

    def testSwitchScene(self) -> None:
        """ Tests if the scene should be switched """
        if self.optionsUI.switchScene():
            # Update switch scene button's text and switch it
            self.optionsUI.updateSceneText(self.state.value)
            self.state = self.getOppositeScene()

    def render(self, surface: Window | Image):
        """ Render the current scene """
        self.scenes[self.state].render(surface)

        self.resourcesUI.render(surface)
        self.optionsUI.render(surface)

    # Getters
    def getOppositeScene(self) -> SceneState:
        """ Returns the opposite scene """
        if self.state == SceneState.BUILDING:
            return SceneState.DUNGEON

        return SceneState.BUILDING
