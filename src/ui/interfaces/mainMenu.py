import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window


class MainMenu(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self, window: Window) -> None:
        """ Create/initialize the main menu """
        super().__init__("mainMenu")

        self.open(window)

    def open(self, window: Window) -> None:
        """ Opens the main menu """
        super().startTransition("visible", window)

    def update(self, window: Window) -> None:
        """ Updates the menu and the scene behind it """
        super().update(window)

        self.checkPlayButton(window)

    def checkPlayButton(self, window: Window) -> None:
        """ Checks if the play button is pressed """
        if self.getElement("play").getActivated():
            self.startTransition("hidden", window)

    def isOpen(self) -> bool: return super().getPosType() == "visible"
