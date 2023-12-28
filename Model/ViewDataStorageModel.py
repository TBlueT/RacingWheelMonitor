from dataclasses import dataclass

@dataclass()
class ViewDataStorageModel:
        speed: int = 0
        gear: int = 0
        rpm: int = 0
        drs: bool = False
        tireTemperature: list[int] = (0, 0, 0, 0)


        maxRpm: int = 0
        ersStore: int = 0
        ersDeployed: int = 0
        ersDeployMode: int = 0

        lap: int = 0
        lapAll: int = 0
        lapTime: float = 0.0

        tireDamage: list[int] = (0, 0, 0, 0)





