import traceback
import logging
from src.ui.interfaces.baseUI import BaseUI


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
            logger.error(f"{message}:\n\n{self.error}\n")

        # Append error to file
        with open(self.ERRORS_FILE, "a") as f:
            f.write(f"{message}:\n{self.error}\n\n")

    def __init__(self) -> None:
        super().__init__("errorUI")

    def update(self) -> None:
        """ Handles button presses if an error is showing """
        if self.errored:
            super().startTransition("visible")

        super().startTransition("hidden")

    # Getters
    @classmethod
    def isRecoverable(cls) -> bool:
        return cls.recoverable
