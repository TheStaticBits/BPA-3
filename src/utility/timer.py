import logging

from src.window import Window


class Timer:
    def __init__(self, delay: float) -> None:
        self.log = logging.getLogger(__name__)

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
