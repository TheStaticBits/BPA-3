import logging

from src.window import Window


class Timer:
    """ A simple timer that can be used to
        activate something after a delay """
    log = logging.getLogger(__name__)

    def __init__(self, delay: float) -> None:
        self.delay: float = delay
        self.timer: float = 0

    def update(self, window: Window) -> bool:
        """ Updates timer with the amount of time that
            has passed in the previous frame """
        self.timer += window.getDeltaTime()

    def completed(self) -> bool:
        """ Tests if the timer is complete, and then decrements by the delay.
            This allows for handling senarios in which the timer activated
            several times in a single frame (low FPS) to work fine """
        if (self.timer >= self.delay):
            self.timer -= self.delay
            return True

        return False

    def isDone(self) -> bool:
        """ Returns True if the timer is done,
            without resetting it """
        return self.timer >= self.delay

    def reset(self) -> None:
        """ Resets the timer """
        self.timer = 0

    # Getters
    def getTimeLeft(self) -> float:
        """ Returns the time left on the timer """
        return self.delay - self.timer

    def getPercentDone(self) -> float:
        """ Returns the percent of the timer that has passed """
        return self.timer / self.delay
