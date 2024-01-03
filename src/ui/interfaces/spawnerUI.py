from src.ui.interfaces.baseUI import BaseUI


class SpawnerUI(BaseUI):
    """ Handles the popup menu displayed when a spawner is selected to
        show the different warriors that can be chosen to be spawned """

    def __init__(self) -> None:
        super().__init__("buildings/spawner")
