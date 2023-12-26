import traceback
import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window
from src.utility.image import Image
from src.utility.vector import Vect


class ErrorUI(BaseUI):
    """ Handles the error UI popup for any errors in the game """
    log = logging.getLogger(__name__)

    # Static variables to define the error message
    errored: bool = False
    recoverable: bool = False
    message: str = ""
    error: str = ""

    @classmethod
    def loadStatic(cls, constants) -> None:
        cls.ERRORS_FILE: str = constants["saves"]["log"]["errorsFile"]

    # Static method so any file can easily create an error
    @classmethod
    def create(self, message="", logger=None, recoverable=False) -> None:
        """ Create an error message popup """
        self.errored = True
        self.recoverable = recoverable
        self.message = message
        self.error = traceback.format_exc()

        if logger is not None:
            logger.error(f"{message}:\n\n{self.error}")

        # Append error to file
        with open(self.ERRORS_FILE, "a") as f:
            f.write(f"{message}:\n{self.error}\n\n")

    def __init__(self) -> None:
        super().__init__("errorUI")

        # Load from the errorUI.json file
        self.bgAlpha = super().getData()["bgAlpha"]

    def update(self, window: Window) -> None:
        """ Handles button presses if an error is showing """
        self.checkTransition(window)
        super().update(window)

        # Button detection here
        if super().getElement("xButton").getActivated():
            print("E")
            self.errored = False

    def checkTransition(self, window: Window) -> None:
        """ Check if an error has occurred """
        # A new error occured:
        if self.errored and super().getPosType() == "hidden":
            super().startTransition("visible", window)

            # Setting UI text with updated messages
            super().getElement("errorMsg").setText(self.error)
            super().getElement("desc").setText(self.message)

            if self.recoverable:
                text = "A recoverable error occured:"
            else:
                text = "An unrecoverable error occured:"

            super().getElement("title").setText(text)

        # Exited error screen:
        elif not self.errored and super().getPosType() == "visible":
            super().startTransition("hidden", window)

    def render(self, surface: Window | Image) -> None:
        """ Renders a dark overlay behind the error message """
        if super().isHidden():
            return

        percent = super().getPercentDone()
        if super().getPosType() == "hidden":
            percent = 1 - percent

        # create and render shaded overlay
        surf: Image = Image.makeEmpty(surface.getSize(),
                                      transparent=True)
        surf.fill((0, 0, 0, round(self.bgAlpha * percent)))

        surface.render(surf, Vect(0, 0))

        super().render(surface)

    # Getters
    @classmethod
    def isRecoverable(cls) -> bool:
        return cls.recoverable
