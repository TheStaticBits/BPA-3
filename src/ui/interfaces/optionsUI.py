from src.ui.interfaces.baseUI import BaseUI


class OptionsUI(BaseUI):
    def __init__(self) -> None:
        super().__init__("optionsUI", __name__)

    def switchScene(self) -> bool:
        """ Returns true if the scene should be switched """
        return super().getElement("switchScene").getActivated()

    def updateSceneText(self, text: str):
        """ Capitalizes first letter and sets the button text """
        text = text[0].upper() + text[1:].lower()
        super().getElement("switchScene").getText().setText(text)
