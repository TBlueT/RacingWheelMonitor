from dataclasses import dataclass

@dataclass()
class ViewDataStorageModel:
        speed: int = 0
        gear: int = 0
        rpm: int = 0
        drs: bool = False
        drsAllowed: bool = False
        tireTemperature = [0, 0, 0, 0]


        maxRpm: int = 0
        ersStore: float = 0
        ersDeployed: float = 0
        ersDeployMode: int = 0

        lap: int = 0
        lapAll: int = 0
        lapTime: int = 0

        tireDamage = [0, 0, 0, 0]





