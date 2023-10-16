from src.ui.baseUI import BaseUI

from src.window import Window


class TestUI(BaseUI):
    """ Handles UI surrounding the screen
        when walking around during gameplay """

    def __init__(self) -> None:
        super().__init__("test.json", __name__)

    def update(self, window: Window) -> None:
        super().update(window)

        if super().getElement("exampleButton").getActivated():
            print("Example button pressed")
