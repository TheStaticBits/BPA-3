from src.game import Game
import pygame
pygame.init()

CONSTANTS_FILE: str = "data/constants.json"

g: Game = Game(CONSTANTS_FILE)
g.mainLoop()
