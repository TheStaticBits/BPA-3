from src.entities.buildings.baseBuilding import BaseBuilding
from src.utility.vector import Vect
from src.tileset import Tileset


class Generator(BaseBuilding):
    def __init__(self, type: str, tileset: Tileset, tilePos: Vect) -> None:
        super().__init__(type, tileset, tilePos)

        self.storage: dict = super().getData()[""]
