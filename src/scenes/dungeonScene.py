from src.scenes.baseScene import BaseScene


class DungeonScene(BaseScene):
    def __init__(self, mapFolderName: str) -> None:
        super().__init__(mapFolderName, __name__)
