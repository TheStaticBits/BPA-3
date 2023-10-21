from src.ui.interfaces.baseUI import BaseUI

from src.window import Window


class BuildingsSceneUI(BaseUI):
    """ Handles UI surrounding the screen
        when walking around during gameplay """

    def __init__(self) -> None:
        super().__init__("buildingsSceneUI.json", __name__)

    def update(self, window: Window) -> None:
        super().update(window)

        if super().getElement("exampleButton").getActivated():
            print("Example button pressed")
