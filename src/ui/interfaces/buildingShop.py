from src.ui.interfaces.baseUI import BaseUI

from src.window import Window


class BuildingShop(BaseUI):
    """ Handles building shop UI """

    def __init__(self) -> None:
        super().__init__("buildingsShop", __name__)

    def update(self, window: Window) -> None:
        super().update(window)

        if super().getElement("openShop").getActivated():
            if super().getPosType() == "hidden":
                super().startTransition(window, "visible")
            else:
                super().startTransition(window, "hidden")
