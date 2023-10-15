import src.game
import pygame
pygame.init()

CONSTANTS_FILE: str = "data/constants.json"

g = src.game.Game(CONSTANTS_FILE)
g.mainLoop()
