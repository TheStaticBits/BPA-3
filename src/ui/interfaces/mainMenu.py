import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window


class MainMenu(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self, window: Window) -> None:
        """ Create/initialize the main menu """
        super().__init__("mainMenu")

        # Start transition to visible upon game launch
        # super().startTransition("visible", window)

    def update(self, window: Window) -> None:
        """ Updates the menu and the scene behind it """
        super().update(window)

    def isOpen(self) -> bool: return super().getPosType() == "visible"
