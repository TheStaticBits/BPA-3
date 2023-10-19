import pygame
import logging
import colorlog
import os
import json

from src.utility.vector import Vect

IMG_SCALE = 1


def loadFile(path: str) -> str:
    """ Loads a file from the given path """
    with open(path, "r") as file:
        return file.read()


def loadJSON(path: str) -> dict:
    """ Loads a JSON file from the given path """
    with open(path, "r") as file:
        return json.load(file)


def loadImg(path: str) -> pygame.Surface:
    """ Loads an image from the given path """
    # convert_alpha converts the image to a quicker rendering file format
    # and allows for transparency, unlike the pygame convert() function
    img: pygame.Surface = pygame.image.load(path).convert_alpha()

    if IMG_SCALE != 1:
        # Scales the image by IMG_SCALE
        size: Vect = Vect(img.get_size())
        img = pygame.transform.scale(img, (size * IMG_SCALE).toTuple())

    return img


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
