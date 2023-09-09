import src.game, pygame
pygame.init()

CONSTANTS_FILE = "data/constants.json"

g = src.game.Game(CONSTANTS_FILE)
g.mainLoop()