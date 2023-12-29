import logging
import src.utility.utility as util
from src.utility.timer import Timer
from src.window import Window


class Waves:
    """ Manages waves, delays, spawning enemies, etc. """
    log = logging.getLogger(__name__)

    @classmethod
    def loadStatic(cls, constants: dict) -> None:
        """ Loads the waves JSON file data """
        cls.WAVES_DATA: list = util.loadJSON(constants["waves"]["jsonPath"])

        cls.WAVES_DELAY: float = constants["waves"]["delayBetweenWaves"]

    def __init__(self) -> None:
        """ Sets up wave timers and data """
        self.waveTimer: Timer = Timer(self.WAVES_DELAY)

        self.betweenWaves: bool = False

        self.spawnData: list[dict] = []  # Spawning data for each enemy type
        self.spawnQueue: list[str] = []  # Enemies that have been spawned

        self.loadWave(0)  # Load the first wave

    def loadWave(self, waveNum: int) -> None:
        """ Loads the delay objects for the wave """
        self.waveNum = waveNum

        if waveNum >= len(self.WAVES_DATA):
            self.log.warn("All waves have been completed. Oops!")
            self.waveNum = 0
            return

        for data in self.WAVES_DATA[waveNum]:
            # Create timers (startTimer, spawnTimer)
            # and load data amounts (amount, spawnAmount)

            self.spawnData.append({
                "type": data["type"],
                "amount": data["amount"],  # Total amount to spawn
                "spawnAmount": data["spawnAmount"],  # Amount created per spawn
                "startTimer": Timer(data["startDelay"]),
                "spawnTimer": Timer(data["spawnInterval"]),
            })

    def update(self, window: Window) -> None:
        """ Updates the wave timer """
        if self.betweenWaves:  # Delay timer between waves
            self.waveTimer.update(window)
            if self.waveTimer.completed():
                self.waveTimer.reset()  # Reset timer
                self.betweenWaves = False

                self.loadWave(self.waveNum + 1)  # Load new wave
                self.log.info(f"Starting wave {self.waveNum + 1}")

        else:
            self.updateDelays(window)

    def updateDelays(self, window: Window) -> None:
        """ Updates the delays for the warriors in the wave,
            spawning any if they are ready """

        for data in self.spawnData:
            if data["startTimer"] is not False:
                data["startTimer"].update(window)  # Update timer
                if data["startTimer"].completed():
                    data["startTimer"] = False
                else:
                    continue  # Skip the rest of the loop

            if data["amount"] <= 0:
                continue

            # Start timer is False, so spawn warriors
            data["spawnTimer"].update(window)
            while data["spawnTimer"].completed():
                for _ in range(data["spawnAmount"]):
                    # Spawn enemy
                    self.spawnQueue.append(data["type"])
                    data["amount"] -= 1

        # Test if all enemies have been spawned
        for data in self.spawnData:
            if data["amount"] > 0:
                return

        # all enemies in the wave have spawned, start delay timer
        self.betweenWaves = True

    # Getters
    def getSpawnQueue(self) -> list:
        """ Returns the spawn queue """
        return self.spawnQueue

    # Setters
    def clearQueue(self) -> None:
        """ Clears the spawn queue """
        self.spawnQueue.clear()
