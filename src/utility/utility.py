import logging, os, json


def loadFile(path):
    """ Loads a file from the given path """
    with open(path, "r") as file:
        return file.read()


def loadJSON(path):
    """ Loads a JSON file from the given path """
    with open(path, "r") as file:
        return json.load(file)


def createFolder(folder):
    """ Creates the a folder directory if it hasn't already been created """
    if not os.path.exists(folder):
        os.mkdir(folder)


def setupLogger(constants):
    """ Setting up base Python logger for every file to use """
    # Generate base save folder if it doesn't exist
    createFolder(constants["saves"]["folder"])

    logger = logging.getLogger("") # Getting base logger

    # Getting log level from the constants JSON file
    LOG_LEVEL = constants["saves"]["log"]["level"]

    if LOG_LEVEL == "debug":     logger.setLevel(logging.DEBUG)
    elif LOG_LEVEL == "warning": logger.setLevel(logging.WARNING)
    elif LOG_LEVEL == "info":    logger.setLevel(logging.INFO)

    # Setting up the format of log output
    fileFormat =    logging.Formatter("%(asctime)s - [%(levelname)s] %(name)s (line %(lineno)d): %(message)s")
    consoleFormat = logging.Formatter("[%(levelname)s] %(name)s (line %(lineno)d): \033[1;37m%(message)s\033[1;0m")    

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

    # Add colors to the logger
    # These are using console color escape codes to color the level name output
    # Using f-strings to insert the log level name between the color escape codes
    logging.addLevelName(logging.WARNING, f"\033[1;33m{logging.getLevelName(logging.WARNING)}\033[1;0m")
    logging.addLevelName(logging.ERROR,   f"\033[1;31m{logging.getLevelName(logging.ERROR  )}\033[1;0m")
    logging.addLevelName(logging.INFO,    f"\033[1;37m{logging.getLevelName(logging.INFO   )}\033[1;0m")