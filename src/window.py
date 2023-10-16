import pygame
import logging
import time
import enum

from src.utility.vector import Vect


class InputState(enum.Enum):
    """ Input states for mouse and keyboard inputs """
    INACTIVE = 0  # Not pressed
    JUST_PRESSED = 1  # Frame on which the button was pressed
    PRESSED = 2  # Held down
    RELEASED = 3  # Frame on which the button was released


class Window:
    """ Handles actions regarding the Pygame window object and deltatime """

    # Inputs and what string value they map to in the window.inputs dict
    KEYS: dict = {
        pygame.K_a: "left",  pygame.K_LEFT: "left",
        pygame.K_d: "right", pygame.K_RIGHT: "right",
        pygame.K_w: "up",    pygame.K_UP: "up",
        pygame.K_s: "down",  pygame.K_DOWN: "down",

        pygame.K_SPACE: "space"  # may be temporary
    }

    MOUSE: dict = {
        pygame.BUTTON_LEFT: "left",
        pygame.BUTTON_MIDDLE: "middle",
        pygame.BUTTON_RIGHT: "right"
    }

    def __init__(self, constants) -> None:
        """ Creates the Window object from data in data/constants.json,
            along with deltatime and fps tracking """
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing window")

        # Create pygame window object
        self.MIN_SIZE: Vect = Vect(constants["window"]["minSize"])
        self.windowSize: Vect = self.MIN_SIZE  # Gets updated when resized
        self.vsync: bool = constants["window"]["vsync"]
        self.windowFlags: int = 0

        if constants["window"]["resizable"]:
            self.windowFlags |= pygame.RESIZABLE  # make window resizable

        self.setWindow(self.MIN_SIZE)  # create window

        pygame.display.set_caption(constants["window"]["title"])

        # Clock for fixed framerate (if enabled)
        self.clock: pygame.Clock = pygame.time.Clock()

        # FPS and whether or not to log it
        self.FPS: int = constants["window"]["FPS"]
        self.LOG_FPS: bool = constants["window"]["logFPS"]

        # Deltatime
        self.deltaTime: float = 0
        self.previousTime: float = time.time()

        # For finding the average FPS over each second to output to the console
        self.lastSecondFPS: list[int] = []
        self.frameTimer: float = 0  # Tracks when a second has passed

        self.quit: bool = False

        # Inputs
        self.inputs: dict = {}

        # Set default inputs all to inactive
        for value in self.KEYS.values():
            self.inputs[value] = InputState.INACTIVE

        # Mouse inputs
        self.mousePos: Vect = Vect(0, 0)

        self.mouseButtons: dict = {}
        for value in self.MOUSE.values():
            self.mouseButtons[value] = InputState.INACTIVE

    def setWindow(self, size: Vect) -> None:
        """ Sets up the Pygame window with the given size
            and various settings """
        self.window = pygame.display.set_mode(size.toTuple(),
                                              self.windowFlags,
                                              vsync=self.vsync)

    def update(self) -> None:
        """ Updates the window with what was
            rendered over the previous frame """

        pygame.display.flip()  # Update the window
        self.window.fill((0, 0, 0))  # Clear the window

        # Cap FPS
        if self.FPS > 0 and not self.vsync:
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

    def updateInputs(self, buttons: dict) -> None:
        """ Updates the values of a dict
            to cycle between input states """
        # The inputs are only JUST_PRESSED and RELEASED for one frame,
        # so they need to be updated to PRESSED and INACTIVE
        for key in buttons:
            if buttons[key] == InputState.JUST_PRESSED:
                buttons[key] = InputState.PRESSED

            elif buttons[key] == InputState.RELEASED:
                buttons[key] = InputState.INACTIVE

    def render(self, img: pygame.Surface, pos: Vect,
               area: pygame.Rect = None) -> None:
        """ Renders an image on a window at a given position,
            with a given portion (area) of the image to render if specified """
        self.window.blit(img, pos.toTuple(), area=(area if area else None))

    def drawRect(self, pos: Vect, size: Vect,
                 color: tuple[int, int, int]) -> None:
        """ Draws a rectangle on the window """
        pygame.draw.rect(self.window, color, pygame.Rect(pos.toTuple(),
                                                         size.toTuple()))

    # Getters
    def getDeltaTime(self) -> float:
        """ Returns the time that has elapsed since the previous function """
        return self.deltaTime

    def getMousePos(self) -> Vect: return self.mousePos
    def isClosed(self) -> bool: return self.quit
    def getWindowSize(self) -> Vect: return self.windowSize

    # Keyboard inputs
    def getKey(self, key: str) -> bool:
        return self.inputs[key] == InputState.PRESSED

    def getJustPressed(self, key: str) -> bool:
        return self.inputs[key] == InputState.JUST_PRESSED

    def getKeyReleased(self, key: str) -> bool:
        return self.inputs[key] == InputState.RELEASED

    # Mouse inputs
    def getMouseButton(self, button: str) -> bool:
        return self.mouseButtons[button] == InputState.PRESSED

    def getMouseJustPressed(self, button: str) -> bool:
        return self.mouseButtons[button] == InputState.JUST_PRESSED

    def getMouseReleased(self, button: str) -> bool:
        return self.mouseButtons[button] == InputState.RELEASED
