import logging

import src.utility.utility as util
from src.utility.animation import Animation
from src.utility.vector import Vect
from src.window import Window

class Entity:
    """ Base class for all entities in the game.
        Handles the animation and position """
    
    # Stores any spritesheets used so as to reduce duplicates
    spritesheets = {}
    
    def __init__(self, animData: dict, pos: Vect=Vect()) -> None:
        """ Setup base values. animData must contain "path", "frames", and "delay" keys """
        self.log = logging.getLogger(__name__)

        self.pos = pos

        self.loadSpritesheet(animData["path"])
        self.animation = self.loadAnim(animData)
    
    
    def loadSpritesheet(self, animPath: str) -> None:
        """ Loads spritesheet image at path if it's
            not already in the spritesheets variable """
        if animPath not in self.spritesheets:
            self.log.info(f"Loading animation spritesheet at {animPath}")
            self.spritesheets[animPath] = util.loadImg(animPath)


    def loadAnim(self, animData: dict) -> Animation:
        """ Loads the animation object using a """
        return Animation(self.spritesheets[animData["path"]], 
                         animData["frames"], 
                         animData["delay"])


    def update(self, window: Window) -> None:
        """ Updates the animation """
        self.animation.update(window)
    

    def render(self, window: Window) -> None:
        """ Renders the animation at the entity's current position"""
        self.animation.render(window, self.pos)
    
    
    # Getters
    def getAnim(self) -> Animation: return self.animation

    # Setters
    def setPos(self, pos: Vect) -> None: self.pos = pos

    # Add more when needed