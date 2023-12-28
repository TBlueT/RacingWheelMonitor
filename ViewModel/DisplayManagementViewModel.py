import time, datetime

from PyQt5 import QtCore, QtGui, QtTest

from ViewModel.ImageProcessing import ImageProcessing
from Model.ViewDataStorageModel import ViewDataStorageModel

class DisplayManagementViewModel(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)
    Set_Pixmap = QtCore.pyqtSignal(str, QtGui.QPixmap)
    Set_StyleSheet = QtCore.pyqtSignal(str, str)
    Set_page = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(DisplayManagementViewModel, self).__init__()

        self.ViewDataStorageM = parent.ViewDataStorageM
        self.ViewDataStorageM_Comparison = ViewDataStorageModel()
        self.ImageP = ImageProcessing(parent)

    # def RPMBar_SetMaxRPM(self, maxRpm:int):
    #     self.ImageP.
        self.DisplayUpdateTimeSet = 0.001
        self.DisplayUpdateTime = time.time()

    def run(self):
        while True:
            temp_time = time.time()
            if temp_time - self.DisplayUpdateTime > self.DisplayUpdateTimeSet:
                self.PacketMotionData()
                self.PacketSessionData()
                self.PacketLapData()
                self.PacketCarTelemetryData()
                self.PacketCarStatusData()
                self.PacketFinalClassificationData()
                self.PacketCarDamageData()

                self.DisplayUpdateTime = temp_time

    def PacketMotionData(self):
        pass

    def PacketSessionData(self):
        self.ImageP.RPMBar_setMaxRpm(self.ViewDataStorageM.maxRpm)

    def PacketLapData(self):
        self.CurrentLapTime()


    def CurrentLapTime(self):
        CurrentLapTime = datetime.datetime.utcfromtimestamp(
            self.ViewDataStorageM.lapTime / 1000.0)

        CurrentLapTime_hour = F"{CurrentLapTime.hour}:" if CurrentLapTime.hour >= 10 else F"0{CurrentLapTime.hour}:" if CurrentLapTime.hour != 0 else ""
        CurrentLapTime_minute = F"{CurrentLapTime.minute}:" if CurrentLapTime.minute >= 10 else F"0{CurrentLapTime.minute}:" if CurrentLapTime.minute != 0 or CurrentLapTime.hour != 0 else ""
        CurrentLapTime_second = F"{CurrentLapTime.second}." if CurrentLapTime.second >= 10 else F"0{CurrentLapTime.second}."
        CurrentLapTime_microsecond = F"{str(CurrentLapTime.microsecond)[0:3]}"
        self.Set_Text.emit("LapTimeText",
                           F"{CurrentLapTime_hour}{CurrentLapTime_minute}{CurrentLapTime_second}{CurrentLapTime_microsecond}")
        self.Set_Text.emit("LapsText", F"{self.ViewDataStorageM.lap}/{self.ViewDataStorageM.lapAll}")


    def PacketCarTelemetryData(self):
        if self.Comparison(self.ViewDataStorageM.rpm, self.ViewDataStorageM_Comparison.rpm):
            self.ImageP.RPMBar_RpmFill(self.ViewDataStorageM.rpm)
            self.Set_Text.emit("RPMText", F"{self.ViewDataStorageM.rpm}")
            print(self.ViewDataStorageM_Comparison.rpm)
        self.Set_Text.emit("SpeedText", F"{self.ViewDataStorageM.speed}")

        self.Gear()
        self.Drs()

        for i in range(0, 4):
            self.Set_Text.emit(F"TyresSurfaceTemperature_{i + 1}_Text",
                               F"{self.ViewDataStorageM.tireTemperature[i]}'C")

        self.Set_Pixmap.emit("RPMBar", self.ImageP.RPMBar_GetImg())

    def Gear(self):
        Gear = self.ViewDataStorageM.gear
        Gear = F"{Gear}" if Gear > 0 else "N" if Gear != -1 else "R"
        self.Set_Text.emit("GearText", F"{Gear}")

    def Drs(self):
        if self.ViewDataStorageM.drs:
            self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(0, 255, 0);")

    def PacketCarStatusData(self):
        self.Drs_Available()

        ersDeployMode_text = {0: "None", 1: "Medium", 2: "HotLap", 3: "Overtake"}
        ersDeployMode_num = self.ViewDataStorageM.ersDeployMode
        self.Set_Text.emit("RES_Mode", F"{ersDeployMode_text[ersDeployMode_num]}")

        self.ImageP.ERS_Store_Fill(self.ViewDataStorageM.ersStore)
        self.ImageP.ERS_Deploted_Fill(self.ViewDataStorageM.ersDeployed)

        self.Set_Pixmap.emit("ERS_Store", self.ImageP.ERS_Store_GetImg())
        self.Set_Pixmap.emit("ERS_Deploted", self.ImageP.ERS_Deploted_GetImg())

    def Drs_Available(self):
        drs_allowed = self.ViewDataStorageM.drsAllowed
        drs = self.ViewDataStorageM.drs
        if (not drs) and (drs_allowed == 1):
            self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(255, 0, 0);")
        elif (not drs) and (drs_allowed == 0):
            self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(0, 0, 0);")

    def PacketFinalClassificationData(self):
        pass

    def PacketCarDamageData(self):
        for i, data in enumerate(self.ViewDataStorageM.tireDamage):
            self.Set_Text.emit(F"tyresWear_{i + 1}_Text", F"{int(data)}%")

    def Comparison(self, target, previous):
        if target != previous:
            previous = target
            return True
        else:
            return False
