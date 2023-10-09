import logging

import src.utility.utility as util
from src.utility.animation import Animation
from src.utility.vector import Vect
from src.window import Window

class Entity:
    """ Base class for all entities in the game.
        Handles the animation and position """
    
    # Cache for spritesheets so as to reduce loading the same image twice
    # Key: image path - Value: the spritesheet
    spritesheets: dict = {}
    
    def __init__(self, animData: dict, pos: Vect=Vect()) -> None:
        """ Setup base values. animData must contain "path", "frames", and "delay" keys
            pos is an optional argument which is set to (0, 0) by default """
        
        self.log = logging.getLogger(__name__)

        self.pos: Vect = pos

        self.loadSpritesheet(animData["path"])
        self.animation = self.loadAnim(animData)
    
    
    def loadSpritesheet(self, animPath: str) -> None:
        """ Loads spritesheet image at path if it's
            not already in the spritesheets variable """
        if animPath not in self.spritesheets:
            self.log.info(f"Loading animation spritesheet at {animPath}")
            self.spritesheets[animPath] = util.loadImg(animPath)


    def loadAnim(self, animData: dict) -> Animation:
        """ Loads the animation object """
        return Animation(self.spritesheets[animData["path"]], 
                         animData["frames"], 
                         animData["delay"])


    def update(self, window: Window) -> None:
        """ Updates the animation """
        self.animation.update(window)
    

    def render(self, window: Window, offset: Vect=Vect()) -> None:
        """ Renders the animation at the entity's current position"""
        self.animation.render(window, self.pos + offset)
    
    
    # Getters
    def getAnim(self) -> Animation: return self.animation
    def getPos(self) -> Vect: return self.pos
    def getCenterPos(self) -> Vect:
        """ Returns the center of the entity """
        return self.pos + (self.animation.getSize() / 2)

    # Setters
    def setPos(self, pos: Vect) -> None: self.pos = pos
    def addPos(self, addPos: Vect) -> None:
        self.pos += addPos