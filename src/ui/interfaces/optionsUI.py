import logging
from src.ui.interfaces.baseUI import BaseUI


class OptionsUI(BaseUI):
    """ Handles the options UI in the top right of the screen """
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__("optionsUI")

        super().getElement("pauseButton").setEnabled(False)

    def switchScene(self) -> bool:
        """ Returns true if the scene should be switched """
        return super().getElement("switchScene").getActivated()

    def updateSceneText(self, text: str):
        """ Capitalizes first letter and sets the button text """
        text = text[0].upper() + text[1:].lower()
        super().getElement("switchScene").getText().setText(text)
