import logging

from src.entities.entity import Entity
from src.utility.vector import Vect

class Tile(Entity):
    """ Inherits from Entity, using its update & render functions. 
        Handles any tile-related functionality such as holding whether
        or not a specific tile is occupied """
    
    def __init__(self, pos: Vect, occupied: bool, animData: dict) -> None:
        """ Tile initialization with pos, occupied, and animation info """
        self.log = logging.getLogger(__name__)

        super().__init__(animData, pos)

        # Whether the tile has a building, tree, etc. on it
        self.occupied: bool = occupied
    

    # Getters
    def getOccupied(self) -> bool: return self.occupied

    # Setters
    def setOccupied(self, occupied: bool) -> None: self.occupied = occupied