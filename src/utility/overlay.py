import logging
from src.utility.image import Image
from src.window import Window
from src.utility.vector import Vect


class Overlay:
    """ Handles a UI overlay,
        including shifts in opacity over time """
    log = logging.getLogger(__name__)

    def __init__(self, maxOpacity: int) -> None:
        """ Creates a default empty overlay """
        self.maxOpacity: int = maxOpacity
        self.opacity: int = 0
        self.size: Vect = Vect(1)
        self.makeOverlay()

    def update(self, opacity: int, surface: Window | Image) -> None:
        """ Updates the overlay, changing it if necessary """
        size: Vect = surface.getSize()

        if opacity < 0:
            opacity = self.maxOpacity

        # Update overlay image if anything changed
        if self.opacity != opacity or self.size != size:
            self.opacity = opacity
            self.size = size
            self.makeOverlay()

    def makeOverlay(self) -> None:
        """ Creates the overlay image """
        self.image = Image.makeEmpty(self.size, scale=False,
                                     transparent=True)
        self.image.fill((0, 0, 0))
        self.image.setAlpha(self.opacity)

    def percentOpacity(self, percent: float, reversed: bool = False) -> int:
        """ Gets the opacity from a percent """
        if reversed:
            percent = 1 - percent

        return round(percent * self.maxOpacity)

    def render(self, surface: Window | Image) -> None:
        """ Renders the overlay """
        surface.render(self.image, Vect(0, 0))
