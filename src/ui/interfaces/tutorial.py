import logging
from src.ui.interfaces.baseUI import BaseUI
from src.window import Window
from src.ui.interfaces.errorUI import ErrorUI


class Tutorial(BaseUI):
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create/initialize the tutorial """
        super().__init__("tutorial")

        self.slide: int = 0

        try:
            self.totalSlides: int = super().getData()["slides"]
            self.hideAllBut(0)
        except KeyError:
            ErrorUI.create("Unable to find slides number in tutorial.json",
                           self.log, recoverable=False)

    def hideAllBut(self, currentSlide: int) -> None:
        """ Hides all slides but the current one """
        elements = super().getAllElements()

        for key, element in elements.items():
            number: str = key[:1]

            if number.isdigit():
                if number != str(currentSlide):
                    element.setHidden(True)

    def show(self, window: Window) -> None:
        """ Shows the tutorial ui """
        super().startTransition("visible", window)

    def setSlide(self, newSlide: int) -> None:
        """ Sets the current slide """
        oldSlide = self.slide

        elements = super().getAllElements()

        # Hide the old slide and show the new slide
        for key, element in elements.items():
            number: str = key[:1]

            if number == str(oldSlide):
                element.setHidden(True)
            elif number == str(newSlide):
                element.setHidden(False)

        self.slide = newSlide

    def update(self, window: Window) -> None:
        """ Updates the UI and the buttons """
        super().update(window)

        if super().getElement("closeButton").getActivated():
            super().startTransition("hidden", window)

        self.updateLeftRight()

    def updateLeftRight(self) -> None:
        """ Updates the left and right buttons """
        if super().getElement("left").getActivated():
            print(self.slide)
            if self.slide == 0:
                self.setSlide(self.totalSlides - 1)
            else:
                self.setSlide(self.slide - 1)

        if super().getElement("right").getActivated():
            print(self.slide)
            if self.slide == self.totalSlides - 1:
                self.setSlide(0)
            else:
                self.setSlide(self.slide + 1)
