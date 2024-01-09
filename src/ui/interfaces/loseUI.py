import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window
from src.utility.image import Image
from src.utility.overlay import Overlay


class LoseUI(BaseUI):
    """ UI that shows when the player loses """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create/initialize the lose screen """
        super().__init__("loseUI")

        maxOpacity = super().getData()["bgAlpha"]
        self.overlay = Overlay(maxOpacity)

        self.closed: bool = False

    def show(self, window: Window, score: int) -> None:
        """ Shows the lose screen """
        super().startTransition("visible", window)
        super().getElement("score").setText(f"Wave: {score + 1}")

    def reset(self, window: Window) -> None:
        """ Resets the lose screen """
        super().startTransition("hidden", window)  # No transition
        self.closed = False

    def update(self, window: Window) -> None:
        """ Updates the lose screen """
        super().update(window)

        if not super().isHidden():
            # Update the overlay
            reversed: bool = super().getPosType() == "hidden"
            opacity = self.overlay.percentOpacity(super().getPercentDone(),
                                                  reversed)
            self.overlay.update(opacity, window)

        # Update button
        if super().getElement("close").getActivated():
            self.closed = True

    def render(self, surface: Window | Image) -> None:
        """ Renders the lose screen with an overlay behind it """
        if not super().isHidden():
            self.overlay.render(surface)
            super().render(surface)

    def isClosed(self) -> bool: return self.closed
