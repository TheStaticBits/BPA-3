import traceback
import logging
import webbrowser
import smtplib
from email.mime.text import MIMEText
from base64 import b64decode
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window


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
        """ Load static variables from constants dict,
            these are the error, log, and email data """
        try:
            cls.ERROR_FILE: str = constants["saves"]["log"]["errorsFile"]
            cls.LOG_FILE: str = constants["saves"]["log"]["file"]
        except KeyError:
            cls.create("Unable to find saves -> log -> [errorsFile or "
                       "file] in constants",
                       cls.log)

        try:
            # decode password
            cls.PASSWORD = b64decode(constants["email"]["pwd"]).decode("utf-8")
            cls.EMAIL_SENDER = constants["email"]["sender"]

        except KeyError:
            cls.create("Unable to find email -> [sender or pwd] "
                       "in constants",
                       cls.log)

        # Find number of lines in the log file (so any crash reports
        # will include all lines since the game started)
        with open(cls.LOG_FILE, "r") as f:
            cls.logLines = len(f.readlines())

    # Static method so any file can easily create an error
    @classmethod
    def create(self, message="", logger=None, recoverable=False) -> None:
        """ Create an error message popup """
        if self.errored:
            return

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

    def update(self, window: Window) -> None:
        """ Handles button presses if an error is showing """
        self.checkTransition(window)
        super().update(window)

        if super().isHidden():
            return

        self.updateButtons()

    def updateButtons(self) -> None:
        """ Handles button presses on the error screen """
        if super().getElement("xButton").getActivated():
            self.errored = False

        # Opens error and log files in the default text editor
        if super().getElement("errorFile").getActivated():
            webbrowser.open(self.ERROR_FILE)
        if super().getElement("logFile").getActivated():
            webbrowser.open(self.LOG_FILE)

        # Send report email button!
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
