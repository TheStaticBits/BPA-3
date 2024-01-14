import logging
import colorlog
import os
import json


def loadFile(path: str) -> str:
    """ Loads a file from the given path """
    with open(path, "r") as file:
        return file.read()


def loadJSON(path: str) -> dict:
    """ Loads a JSON file from the given path """
    with open(path, "r") as file:
        return json.load(file)


def clamp(value: float, minimum: float, maximum: float) -> float:
    """ Clamps a value between a minimum and maximum """
    return max(minimum, min(value, maximum))


def createFolder(folder) -> None:
    """ Creates the a folder directory if it hasn't already been created """
    if not os.path.exists(folder):
        os.mkdir(folder)


def setupLogger(constants: dict) -> None:
    """ Setting up base Python logger for every file to use """
    # Generate base save folder if it doesn't exist
    createFolder(constants["saves"]["folder"])

    logger = logging.getLogger("")  # Getting base logger

    # Getting log level from the constants JSON file
    LOG_LEVEL = constants["saves"]["log"]["level"]

    if LOG_LEVEL == "debug":
        logger.setLevel(logging.DEBUG)
    elif LOG_LEVEL == "warning":
        logger.setLevel(logging.WARNING)
    elif LOG_LEVEL == "info":
        logger.setLevel(logging.INFO)

    # Setting up the format of log output
    fileFormat = logging.Formatter(
        "%(asctime)s - [%(levelname)s] %(name)s (line %(lineno)d): %(message)s"
    )

    # Using the colorlog module to color the log level name
    # with %(log_color)s and %(reset)s
    consoleFormat = colorlog.ColoredFormatter(
        "[%(log_color)s%(levelname)s%(reset)s]"
        " %(name)s (line %(lineno)d): %(log_color)s%(message)s%(reset)s"
    )

    # Getting log file from the constants JSON file
    LOG_FILE = constants["saves"]["log"]["file"]

    # Create handlers for outputting to file and console
    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(fileFormat)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(consoleFormat)

    # Add the handlers to the logger
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
