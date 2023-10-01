import pygame, logging, time

from src.utility.vector import Vect

class Window:
    """ Handles actions regarding the Pygame window object and deltatime """

    # Inputs and what string value they map to in the window.inputs dict
    KEYS: dict = {
        pygame.K_a: "left",  pygame.K_LEFT: "left",
        pygame.K_d: "right", pygame.K_RIGHT: "right",
        pygame.K_w: "up",    pygame.K_UP: "up",
        pygame.K_s: "down",  pygame.K_DOWN: "down"
    }

    def __init__(self, constants) -> None:
        """ Creates the Window object from data in data/constants.json,
            along with deltatime and fps tracking """
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing window")
        
        self.window: pygame.Surface = pygame.display.set_mode(constants["window"]["size"])
        pygame.display.set_caption(constants["window"]["title"])

        self.clock: pygame.Clock = pygame.time.Clock()

        self.FPS: int = constants["window"]["FPS"]
        self.LOG_FPS: bool = constants["window"]["logFPS"]

        self.deltaTime: float = 0
        self.previousTime: float = time.time()

        # For finding the average FPS over each second to output to the console
        self.lastSecondFPS: list[int] = [] 
        self.frameTimer: float = 0 # Used to keep track of when a second has passed

        self.quit: bool = False

        # Inputs
        self.inputs: dict = {}
        
        # Set default inputs all to false
        for value in self.KEYS.values():
            self.inputs[value] = False
        
        # Mouse inputs
        self.mousePos: Vect = Vect(0, 0)
        self.mouseButtons: dict = { 1: False, 2: False, 3: False } # Left, middle, right clicking
    

    def update(self) -> None:
        """ Updates the window with what was rendered over the previous frame """

        pygame.display.flip() # Update the window
        self.window.fill((0, 0, 0)) # Clear the window

        # Cap FPS
        if self.FPS > 0:
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
                avgDeltaTimes = sum(self.lastSecondFPS) / len(self.lastSecondFPS)

                self.log.info(f"{round(avgDeltaTimes, 2)} FPS")
                self.lastSecondFPS.clear()
        
    
    def handleInputs(self) -> None:
        """ Handle any window inputs """

        # Mouse input
        self.mousePos = Vect(pygame.mouse.get_pos())
        self.mouseButtons[1], self.mouseButtons[2], self.mouseButtons[3] = pygame.mouse.get_pressed()
        
        # Iterate through all pygame-given events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.log.info("Exiting game")
                self.quit = True
            
            # Handle keydown/keyup inputs
            elif event.type == pygame.KEYDOWN:
                if event.key in self.KEYS:
                    self.inputs[self.KEYS[event.key]] = True # self.KEYS gets the string name of the input
            
            elif event.type == pygame.KEYUP:
                if event.key in self.KEYS:
                    self.inputs[self.KEYS[event.key]] = False
    

    def render(self, img: pygame.Surface, pos: Vect, area: pygame.Rect = None) -> None:
        """ Renders an image on a window at a given position,
            with a given portion of the image to render if specified """
        self.window.blit(img, pos.toTuple(), area=(area if area else None))
    

    # Getters
    def getDeltaTime(self) -> float:
        """ Returns the time that has elapsed since the previous function """
        return self.deltaTime

    def getMousePos(self) -> Vect: return self.mousePos
    def getMouseButton(self, button: int) -> bool: return self.mouseButtons[button]
    def getKey(self, key: str) -> bool: return self.inputs[key]

    def isClosed(self) -> bool: return self.quit