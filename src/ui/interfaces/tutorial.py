import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window


class Tutorial(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create/initialize the tutorial """
        super().__init__("tutorial")

    def show(self, window: Window) -> None:
        """ Shows the tutorial ui """
        super().startTransition("visible", window)

    def update(self, window: Window) -> None:
        """ Updates the UI and the buttons """
        super().update(window)

        if super().getElement("closeButton").getActivated():
            super().startTransition("hidden", window)
