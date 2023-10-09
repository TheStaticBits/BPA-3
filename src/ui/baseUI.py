import pygame, logging

class BaseUI:
    """ All UI interfaces inherit from this class,
        which creates and handles UI elements given
        the JSON data for them. """

    def __init__(self):
        self.log = logging.getLogger(__name__)

