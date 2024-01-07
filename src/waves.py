import logging
import src.utility.utility as util
from src.utility.timer import Timer
from src.window import Window
from src.entities.warrior import Warrior


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
        self.spawnQueue: list[Warrior] = []  # Enemies that have been spawned

        self.loadWave(0)  # Load the first wave

        self.lost: bool = False

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
                "level": data["level"],  # Level of warrior to spawn
                "amount": data["amount"],  # Total amount to spawn
                "spawnAmount": data["spawnAmount"],  # Amount created per spawn
                "startTimer": Timer(data["startDelay"]),
                "spawnTimer": Timer(data["spawnInterval"]),
            })

    def update(self, window: Window,
               allies: list[Warrior], enemies: list[Warrior]) -> None:
        """ Updates the wave timer """
        if self.betweenWaves:  # Delay timer between waves
            # During the period between waves allies cannot spawn
            allies.clear()

            self.waveTimer.update(window)
            if self.waveTimer.completed():
                self.waveTimer.reset()  # Reset timer
                self.betweenWaves = False

                self.loadWave(self.waveNum + 1)  # Load new wave
                self.log.info(f"Starting wave {self.waveNum + 1}")

        else:
            self.updateDelays(window)
            self.testEndPeriod(allies, enemies)

    def updateDelays(self, window: Window) -> None:
        """ Updates the delays for the warriors in the wave,
            spawning any if they are ready """
        # Iterating through the data for each enemy type being spawned
        # in the wave
        for data in self.spawnData:
            if data["startTimer"] is not False:
                data["startTimer"].update(window)  # Update timer
                if data["startTimer"].completed():
                    data["startTimer"] = False
                else:
                    continue  # Skip the rest of the loop

            # Start timer is False, so spawn warriors
            data["spawnTimer"].update(window)
            while data["spawnTimer"].completed():
                for _ in range(data["spawnAmount"]):
                    # Amount left to spawn of the warrior type is zero.
                    if data["amount"] <= 0:
                        break

                    # Spawn enemy
                    self.spawnWarrior(data["type"], data["level"])
                    data["amount"] -= 1

    def testEndPeriod(self, allies: list[Warrior],
                      enemies: list[Warrior]) -> None:
        """ Tests the period between waves """
        # Test if all enemies have been spawned
        for data in self.spawnData:
            if data["amount"] > 0:
                return

        # During the period between the last enemy being spawned
        # and the last enemy dying, test the following conditions:

        # No enemies left, so start delay between waves
        if len(enemies) == 0:
            self.betweenWaves = True
            self.log.info(
                "All enemies have died. Starting delay between waves."
            )

        # No allies left on any given frame, so the player lost
        if len(allies) == 0:
            self.log.info("All allies have died. You lose!")
            self.lost = True
            return

    def spawnWarrior(self, warriorType: str, level: int) -> None:
        """ Spawns a warrior by adding it to the queue """
        self.spawnQueue.append(Warrior(warriorType, level, False))

    def clearSpawnQueue(self) -> None:
        """ Clears the spawn queue """
        self.spawnQueue.clear()

    # Geters
    def getWaveNum(self) -> int: return self.waveNum
    def getSpawnQueue(self) -> list[Warrior]: return self.spawnQueue
    def hasLost(self) -> bool: return self.lost
