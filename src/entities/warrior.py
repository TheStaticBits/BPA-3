from src.entities.entity import Entity
from src.window import Window
from src.utility.vector import Vect
import src.utility.utility as util


class Warrior(Entity):
    """ Handles warrior functionality,
        including movement and pathfinding """

    WARRIOR_DICT: dict = None

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the warrior data JSON file """
        cls.WARRIOR_DICT = util.loadJSON(constants["warriors"]["jsonPath"])

    def __init__(self, type: str) -> None:
        """ Setup position, animation, etc. """
        super().__init__(self.WARRIOR_DICT[type]["anim"], __name__,
                         Vect(300, 300))

    def update(self, window: Window) -> None:
        super().update(window)
