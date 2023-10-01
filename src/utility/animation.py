import pygame, logging

from src.window import Window
from src.utility.vector import Vect
from src.utility.timer import Timer

class Animation:
    """ Class for handling animations, 
        including updating and rendering.
        Only works with horizontal spritesheets """
    
    def __init__(self, spritesheet: pygame.Surface, frameCount: int, delay: float):
        """ Sets initial values for the animation """
        self.log = logging.getLogger(__name__)

        self.spritesheet = spritesheet
        self.timer = Timer(delay)

        if spritesheet.get_width() % frameCount != 0:
            self.log.error("Spritesheet width is not divisible by frame count")

        self.frameSize = Vect(spritesheet.get_width() / frameCount, spritesheet.get_height())

        self.frameCount = frameCount
        self.currentFrame: int = 0
    

    def update(self, window: Window):
        """ Updates animation timer and frame if necessary """
        self.timer.update(window)

        # while the timer is completed (allows for low FPS)
        while self.timer.completed():
            self.currentFrame += 1

            if self.currentFrame >= self.frameCount:
                self.currentFrame = 0
        
    
    def render(self, window: Window, pos: Vect):
        """ Renders the portion of the animation spritesheet
            that's the current frame to the window """
        
        # Gets the coordinates and size of the current frame of the spritesheet
        area = pygame.Rect(self.currentFrame * self.frameSize.x, 0, 
                           self.frameSize.x, self.frameSize.y)

        window.render(self.spritesheet, pos, area=area)
    

    # Getters
    def getSize(self) -> Vect: return self.frameSize