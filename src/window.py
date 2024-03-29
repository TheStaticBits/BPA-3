import pygame
import logging
import time
import enum

from src.utility.vector import Vect
from src.utility.image import Image


class InputState(enum.Enum):
    """ Input states for mouse and keyboard inputs """
    INACTIVE = 0  # Not pressed
    JUST_PRESSED = 1  # Frame on which the button was pressed
    PRESSED = 2  # Held down
    RELEASED = 3  # Frame on which the button was released


class Window:
    """ Handles actions regarding the Pygame window object and deltatime """
    log = logging.getLogger(__name__)

    # Inputs and what string value they map to in the window.inputs dict
    KEYS: dict[int, str] = {
        pygame.K_a: "left",  pygame.K_LEFT: "left",
        pygame.K_d: "right", pygame.K_RIGHT: "right",
        pygame.K_w: "up",    pygame.K_UP: "up",
        pygame.K_s: "down",  pygame.K_DOWN: "down",

        pygame.K_LSHIFT: "shift", pygame.K_RSHIFT: "shift",
        pygame.K_ESCAPE: "esc"
    }

    MOUSE: dict[int, str] = {
        pygame.BUTTON_LEFT: "left",
        pygame.BUTTON_MIDDLE: "middle",
        pygame.BUTTON_RIGHT: "right"
    }

    # Static methods
    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads static variables from constants """
        try:
            # Minimum size of the window when resizing
            cls.MIN_SIZE: Vect = Vect(constants["window"]["minSize"])
        except KeyError:
            # avoid circular import
            from src.ui.interfaces.errorUI import ErrorUI
            ErrorUI.create("Unable to find window -> minSize in constants. "
                           "Defaulting to (900, 600)",
                           cls.log)
            cls.MIN_SIZE: Vect = Vect(900, 600)

        try:
            # Whether or not to use vsync
            cls.VSYNC: bool = constants["window"]["vsync"]
        except KeyError:
            ErrorUI.create("Unable to find window -> vsync in constants. "
                           "Defaulting to False",
                           cls.log)
            cls.VSYNC: bool = False

        try:
            # FPS and whether or not to log it
            cls.FPS: int = constants["window"]["FPS"]
            cls.LOG_FPS: bool = constants["window"]["logFPS"]
        except KeyError:
            ErrorUI.create("Unable to find window -> [FPS or logFPS] "
                           "in constants. Defaulting to 60 FPS and False",
                           cls.log)
            cls.FPS: int = 60
            cls.LOG_FPS: bool = False

        try:
            # Whether or not the window should be resizable
            cls.RESIZABLE: bool = constants["window"]["resizable"]
        except KeyError:
            ErrorUI.create("Unable to find window -> resizable in constants. "
                           "Defaulting to False",
                           cls.log)
            cls.RESIZABLE: bool = False

        try:
            cls.WINDOW_TITLE: str = constants["window"]["title"]
            cls.WINDOW_ICON: str = constants["window"]["icon"]
        except KeyError:
            ErrorUI.create("Unable to find window -> [title or icon] "
                           "in constants. Defaulting to 'Game' and none",
                           cls.log)
            cls.WINDOW_TITLE: str = "Game"
            cls.WINDOW_ICON: str = ""

    def __init__(self) -> None:
        """ Creates the Window object from data in data/constants.json,
            along with deltatime and fps tracking """
        self.log.info("Initializing window")

        # Create pygame window object
        self.windowSize: Vect = self.MIN_SIZE  # Gets updated when resized
        self.windowFlags: int = 0

        if self.RESIZABLE:
            self.windowFlags |= pygame.RESIZABLE  # make window resizable

        self.setWindow(self.MIN_SIZE)  # create window

        # Set window title
        pygame.display.set_caption(self.WINDOW_TITLE)

        # Set window icon if it has a path
        if self.WINDOW_ICON != "":
            icon: Image = Image(self.WINDOW_ICON, scale=False)
            pygame.display.set_icon(icon.getSurf())

        # Clock for fixed framerate (if enabled)
        self.clock: pygame.Clock = pygame.time.Clock()

        # Deltatime
        self.deltaTime: float = 0
        self.previousTime: float = time.time()

        # For finding the average FPS over each second to output to the console
        self.lastSecondFPS: list[int] = []
        self.frameTimer: float = 0  # Tracks when a second has passed

        self.quit: bool = False

        # Inputs
        self.inputs: dict[str, InputState] = {}

        # Set default inputs all to inactive
        for value in self.KEYS.values():
            self.inputs[value] = InputState.INACTIVE

        # Mouse inputs
        self.mousePos: Vect = Vect(0, 0)

        self.mouseButtons: dict[str, InputState] = {}
        for value in self.MOUSE.values():
            self.mouseButtons[value] = InputState.INACTIVE

        # Hide inputs
        self.hideInputs: bool = False

    def setWindow(self, size: Vect) -> None:
        """ Sets up the Pygame window with the given size
            and various settings """
        self.window = pygame.display.set_mode(size.toTuple(),
                                              self.windowFlags,
                                              vsync=self.VSYNC)

    def update(self) -> None:
        """ Updates the window with what was
            rendered over the previous frame """

        pygame.display.flip()  # Update the window
        self.window.fill((0, 0, 0))  # Clear the window

        # Cap FPS
        if self.FPS > 0 and not self.VSYNC:
            self.clock.tick(self.FPS)

        # Deltatime is the time that has elapsed since the previous function
        # Any movement is multiplied by it to make it framerate independent
        currentTime: float = time.time()
        self.deltaTime = currentTime - self.previousTime
        self.previousTime = currentTime

        self.frameTimer += self.deltaTime

        if self.LOG_FPS:
            if self.deltaTime != 0:
                # Changes deltatime into FPS
                self.lastSecondFPS.append(1 / self.deltaTime)

            if self.frameTimer >= 1:
                self.frameTimer -= 1

                # Finds the average FPS over the last second
                average = sum(self.lastSecondFPS) / len(self.lastSecondFPS)

                # Rounds to 2 decimal places
                self.log.info(f"{round(average, 2)} FPS")
                self.lastSecondFPS.clear()

    def handleInputs(self) -> None:
        """ Handle any window inputs """

        # Mouse input
        self.mousePos = Vect(pygame.mouse.get_pos())

        # Update inputs
        self.updateInputs(self.inputs)
        self.updateInputs(self.mouseButtons)

        # Iterate through all pygame-given events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.log.info("Exiting game")
                self.quit = True

            # Handle keydown/keyup inputs
            elif event.type == pygame.KEYDOWN:
                if event.key in self.KEYS:
                    # self.KEYS[event.key] gets the string name of the input
                    buttonType: str = self.KEYS[event.key]
                    self.inputs[buttonType] = InputState.JUST_PRESSED

            elif event.type == pygame.KEYUP:
                if event.key in self.KEYS:
                    buttonType: str = self.KEYS[event.key]
                    self.inputs[buttonType] = InputState.RELEASED

            # Handle mouse button inputs
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in self.MOUSE:
                    buttonType: str = self.MOUSE[event.button]
                    self.mouseButtons[buttonType] = InputState.JUST_PRESSED

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.MOUSE:
                    buttonType: str = self.MOUSE[event.button]
                    self.mouseButtons[buttonType] = InputState.RELEASED

            # Window resize
            elif event.type == pygame.VIDEORESIZE:
                self.windowSize = Vect(self.window.get_size())

                # Set minimum window size
                if self.windowSize.x < self.MIN_SIZE.x:
                    self.setWindow(Vect(self.MIN_SIZE.x, self.windowSize.y))

                elif self.windowSize.y < self.MIN_SIZE.y:
                    self.setWindow(Vect(self.windowSize.x, self.MIN_SIZE.y))

    def updateInputs(self, buttons: dict[str, InputState]) -> None:
        """ Updates the values of a dict
            to cycle between input states """
        # The inputs are only JUST_PRESSED and RELEASED for one frame,
        # so they need to be updated to PRESSED and INACTIVE
        for key in buttons:
            if buttons[key] == InputState.JUST_PRESSED:
                buttons[key] = InputState.PRESSED

            elif buttons[key] == InputState.RELEASED:
                buttons[key] = InputState.INACTIVE

    def render(self, img: Image, pos: Vect,
               area: pygame.Rect = None) -> None:
        """ Renders an image on a window at a given position,
            with a given portion (area) of the image to render if specified.
            Renders the image with the image scale specified in constants """
        self.window.blit(img.getSurf(), pos.toTuple(), area=area)

    def drawRect(self, pos: Vect, size: Vect,
                 color: tuple[int, int, int]) -> None:
        """ Draws a rectangle on the window """
        rect = pygame.Rect(pos.toTuple(), size.toTuple())
        pygame.draw.rect(self.window, color, rect)

    # Getters
    def getDeltaTime(self) -> float:
        """ Returns the time that has elapsed since the previous function """
        return self.deltaTime

    def getMousePos(self) -> Vect:
        """ Returns the mouse position """
        if self.hideInputs:
            return Vect()
        return self.mousePos

    def isClosed(self) -> bool: return self.quit
    def getSize(self) -> Vect: return self.windowSize

    # Keyboard inputs
    def getKey(self, key: str) -> bool:
        return self.inputs[key] == InputState.PRESSED \
            and not self.hideInputs

    def getJustPressed(self, key: str) -> bool:
        return self.inputs[key] == InputState.JUST_PRESSED \
            and not self.hideInputs

    def getKeyReleased(self, key: str) -> bool:
        return self.inputs[key] == InputState.RELEASED \
            and not self.hideInputs

    # Mouse inputs
    def getMouseButton(self, button: str) -> bool:
        return self.mouseButtons[button] == InputState.PRESSED \
            and not self.hideInputs

    def getMouseJustPressed(self, button: str) -> bool:
        """ Returns whether or not the mouse button was just pressed """
        if self.hideInputs:
            return False

        # Only allows it to be detected once
        # This makes it so you can't click "through" a UI,
        # both a button on the UI and a thing behind it, for example.
        if self.mouseButtons[button] == InputState.JUST_PRESSED:
            self.mouseButtons[button] = InputState.PRESSED
            return True
        return False

    def getMouseReleased(self, button: str) -> bool:
        return self.mouseButtons[button] == InputState.RELEASED \
            and not self.hideInputs

    # Setters
    def setHideInputs(self, hide: bool) -> None:
        """ Sets whether or not to hide inputs """
        self.hideInputs = hide
