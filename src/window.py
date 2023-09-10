import pygame, logging, time

class Window:
    def __init__(self, constants):
        self.log = logging.getLogger(__name__)

        self.log.info("Initializing window")
        
        self.window = pygame.display.set_mode(constants["window"]["size"])
        pygame.display.set_caption(constants["window"]["title"])

        self.clock = pygame.time.Clock()

        self.FPS = constants["window"]["FPS"]
        self.LOG_FPS = constants["window"]["logFPS"] # True/False

        self.deltaTime = 0
        self.previousTime = time.time()

        # For finding the average FPS over each second to output to the console
        self.lastSecondFPS = [] 
        self.frameTimer = 0 # Used to keep track of when a second has passed

        self.quit = False
    

    def update(self):
        """ Updates the window with what was rendered over the previous frame """

        pygame.display.flip() # Update the window
        self.window.fill((0, 0, 0)) # Clear the window

        # Cap FPS
        if self.FPS > 0:
            self.clock.tick(self.FPS)

        # Deltatime is the time that has elapsed since the previous function
        # Any movement is multiplied by it to make it framerate independent
        currentTime = time.time()
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
        
    
    def handleInputs(self):
        """ Handle any window inputs """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.log.info("Exiting game")
                self.quit = True
    

    # Getters
    def getDeltaTime(self):
        """ Returns the time that has elapsed since the previous function """
        return self.deltaTime

    def isClosed(self): return self.quit