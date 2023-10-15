from src.ui.baseUI import BaseUI


class TestUI(BaseUI):
    """ Handles UI surrounding the screen
        when walking around during gameplay """

    def __init__(self) -> None:
        super().__init__("test.json", __name__)
