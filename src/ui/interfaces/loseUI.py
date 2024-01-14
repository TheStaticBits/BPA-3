import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window


class LoseUI(BaseUI):
    """ UI that shows when the player loses """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create/initialize the lose screen """
        super().__init__("loseUI")

        self.closed: bool = False

    def show(self, window: Window, score: int) -> None:
        """ Shows the lose screen """
        super().startTransition("visible", window)
        super().getElement("score").setText(f"Wave: {score + 1}")

    def reset(self, window: Window) -> None:
        """ Resets the lose screen """
        super().startTransition("hidden", window)
        self.closed = False

    def update(self, window: Window) -> None:
        """ Updates the lose screen """
        super().update(window)

        # Update button
        if super().getElement("close").getActivated():
            self.closed = True

    def pressedClosed(self) -> bool: return self.closed
    def isOpen(self) -> bool: return super().getPosType() == "visible"
