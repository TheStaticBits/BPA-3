from src.ui.interfaces.baseUI import BaseUI
from src.entities.buildings.spawner import Spawner
from src.window import Window
from src.entities.warrior import Warrior
from src.utility.image import Image
from src.utility.animation import Animation
from src.utility.vector import Vect


class SpawnerUI(BaseUI):
    """ Handles the popup menu displayed when a spawner is selected to
        show the different warriors that can be chosen to be spawned """

    def __init__(self) -> None:
        super().__init__("buildings/spawnerSelect")

        self.warriorData: dict = Warrior.WARRIOR_DICT
        self.building: Spawner = None
        self.warriorImgs: dict[str, Image] = {}

    def show(self, building: Spawner, window: Window) -> None:
        """ Shows the UI and updates the elements on screen """
        super().startTransition("visible", window)
        self.building: Spawner = building
        self.setDisplayed()
        self.checkDisabled()

    def setDisplayed(self) -> None:
        """ Updates the elements on screen """
        warriorType: str = self.building.getSpawnType()
        warriorData = self.warriorData[warriorType]

        if warriorType not in self.warriorImgs:
            # Load animation for warrior
            animData = warriorData["allyAnim"]
            anim: Animation = Animation(animData["path"],
                                        animData["frames"],
                                        animData["delay"])
            # Set image to the first frame of the animation
            self.warriorImgs[warriorType] = anim.getFrame(0)

        # Set image being displayed
        super().getElement("warriorImg").setImg(
            self.warriorImgs[warriorType]
        )

        # Set warrior name and description
        super().getElement("warriorName").setText(warriorData["name"])
        super().getElement("description").setText(warriorData["description"])

    def hide(self, window: Window) -> None:
        super().startTransition("hidden", window)
        self.building = None

    def update(self, window: Window, offset: Vect = Vect()) -> None:
        """ Updates the UI and its button functionalities """
        super().update(window, offset)

        self.checkLeftRight()

    def checkLeftRight(self) -> None:
        """ Checks the left and right buttons and manages
            their functionality """
        if super().getElement("left").getActivated():
            # Set the current warrior to the previous warrior
            self.chooseWarrior(self.getWarriorOffset(-1))

        if super().getElement("right").getActivated():
            # Set the current warrior to the next warrior
            self.chooseWarrior(self.getWarriorOffset(1))

    def getWarriorOffset(self, offset: int) -> str:
        """ Gets the warrior at an index offset from the current warrior """
        unlocked: list[str] = self.building.getUnlocked()
        warriorIndex: int = self.building.getWarriorIndex()
        return unlocked[warriorIndex + offset]

    def chooseWarrior(self, warriorType: str = None) -> None:
        """ Chooses the warrior to spawn """
        if warriorType is not None:
            self.building.chooseWarrior(warriorType)
        self.setDisplayed()
        self.checkDisabled()

    def checkDisabled(self) -> None:
        """ Checks information to find whether or not the right and left
            buttons should be disabled """
        warriorIndex: int = self.building.getWarriorIndex()
        super().getElement("left").setEnabled(warriorIndex != 0)
        super().getElement("right").setEnabled(
            warriorIndex != len(self.building.getUnlocked()) - 1
        )
