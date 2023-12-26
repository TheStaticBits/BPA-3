import traceback
import logging
import webbrowser
import smtplib
from email.mime.text import MIMEText
from base64 import b64decode
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
        cls.ERROR_FILE: str = constants["saves"]["log"]["errorsFile"]
        cls.LOG_FILE: str = constants["saves"]["log"]["file"]
        cls.EMAIL_SENDER = constants["email"]["sender"]

        # decode password
        cls.PASSWORD = b64decode(constants["email"]["pwd"]).decode("utf-8")

        # Find number of lines in the log file (so any crash reports
        # will include all lines since the game started)
        with open(cls.LOG_FILE, "r") as f:
            cls.logLines = len(f.readlines())

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
        with open(self.ERROR_FILE, "a") as f:
            f.write(f"{message}:\n{self.error}\n\n")

    def __init__(self) -> None:
        super().__init__("errorUI")

        # Load from the errorUI.json file
        self.bgAlpha = super().getData()["bgAlpha"]

    def update(self, window: Window) -> None:
        """ Handles button presses if an error is showing """
        self.checkTransition(window)
        super().update(window)

        self.updateButtons()

    def updateButtons(self) -> None:
        """ Handles button presses on the error screen """
        if super().getElement("xButton").getActivated():
            self.errored = False

        if super().getElement("errorFile").getActivated():
            webbrowser.open(self.ERROR_FILE)

        if super().getElement("logFile").getActivated():
            webbrowser.open(self.LOG_FILE)

        if super().getElement("sendEmail").getActivated():
            self.emailCrashReport()

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
                super().getElement("xButton").setHidden(False)
            else:
                text = "An unrecoverable error occured:"
                super().getElement("xButton").setHidden(True)

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

    def emailCrashReport(self):
        """ Sends an email to the developer with the crash report """
        self.log.info("Sending crash report email...")

        # Gets the logs since the game started
        with open(self.LOG_FILE, "r") as f:
            log = f.readlines()[self.logLines:]
        log = "\n".join(log)

        msgText = f"Error:\n{self.error}\n\nLog:\n{log}"

        # Creating email object
        msgObj = MIMEText(msgText)
        msgObj["Subject"] = self.message
        msgObj["From"] = self.EMAIL_SENDER
        msgObj["To"] = self.EMAIL_SENDER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as sender:
            sender.login(self.EMAIL_SENDER, self.PASSWORD)
            sender.send_message(msgObj)

    # Getters
    @classmethod
    def isRecoverable(cls) -> bool:
        return cls.recoverable
