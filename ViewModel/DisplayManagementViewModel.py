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
            self.PacketMotionData()
            self.PacketSessionData()
            self.PacketLapData()
            self.PacketCarTelemetryData()
            self.PacketCarStatusData()
            self.PacketFinalClassificationData()
            self.PacketCarDamageData()

            time.sleep(0.001)

    def PacketMotionData(self):
        pass

    def PacketSessionData(self):
        if self.ViewDataStorageM.maxRpm != self.ViewDataStorageM_Comparison.maxRpm:
            self.ImageP.RPMBar_setMaxRpm(self.ViewDataStorageM.maxRpm)
            self.ViewDataStorageM_Comparison.maxRpm = self.ViewDataStorageM.maxRpm

    def PacketLapData(self):
        self.CurrentLapTime()


    def CurrentLapTime(self):
        if self.ViewDataStorageM.lapTime != self.ViewDataStorageM_Comparison.lapTime:
            CurrentLapTime = datetime.datetime.utcfromtimestamp(
                self.ViewDataStorageM.lapTime / 1000.0)

            CurrentLapTime_hour = F"{CurrentLapTime.hour}:" if CurrentLapTime.hour >= 10 else F"0{CurrentLapTime.hour}:" if CurrentLapTime.hour != 0 else ""
            CurrentLapTime_minute = F"{CurrentLapTime.minute}:" if CurrentLapTime.minute >= 10 else F"0{CurrentLapTime.minute}:" if CurrentLapTime.minute != 0 or CurrentLapTime.hour != 0 else ""
            CurrentLapTime_second = F"{CurrentLapTime.second}." if CurrentLapTime.second >= 10 else F"0{CurrentLapTime.second}."
            CurrentLapTime_microsecond = F"{str(CurrentLapTime.microsecond)[0:3]}"
            self.Set_Text.emit("LapTimeText",
                               F"{CurrentLapTime_hour}{CurrentLapTime_minute}{CurrentLapTime_second}{CurrentLapTime_microsecond}")

        self.ViewDataStorageM_Comparison.lapTime = self.ViewDataStorageM.lapTime

        if self.ViewDataStorageM.lap != self.ViewDataStorageM_Comparison.lap:
            self.Set_Text.emit("LapsText", F"{self.ViewDataStorageM.lap}/{self.ViewDataStorageM.lapAll}")
            self.ViewDataStorageM_Comparison.lap = self.ViewDataStorageM.lap


    def PacketCarTelemetryData(self):
        if self.ViewDataStorageM.rpm != self.ViewDataStorageM_Comparison.rpm:
            self.ImageP.RPMBar_RpmFill(self.ViewDataStorageM.rpm)
            self.Set_Text.emit("RPMText", F"{self.ViewDataStorageM.rpm}")
            self.Set_Pixmap.emit("RPMBar", self.ImageP.RPMBar_GetImg())
            self.ViewDataStorageM_Comparison.rpm = self.ViewDataStorageM.rpm

        if self.ViewDataStorageM.speed != self.ViewDataStorageM_Comparison.speed:
            self.Set_Text.emit("SpeedText", F"{self.ViewDataStorageM.speed}")
            self.ViewDataStorageM_Comparison.speed = self.ViewDataStorageM.speed


        self.Gear()
        self.Drs()

        if self.ViewDataStorageM.tireTemperature != self.ViewDataStorageM_Comparison.tireTemperature:
            for i in range(0, 4):
                self.Set_Text.emit(F"TyresSurfaceTemperature_{i + 1}_Text",
                                   F"{self.ViewDataStorageM.tireTemperature[i]}'C")
            self.ViewDataStorageM_Comparison.tireTemperature = self.ViewDataStorageM.tireTemperature

    def Gear(self):
        if self.ViewDataStorageM.gear != self.ViewDataStorageM_Comparison.gear:
            Gear = self.ViewDataStorageM.gear
            Gear = F"{Gear}" if Gear > 0 else "N" if Gear != -1 else "R"
            self.Set_Text.emit("GearText", F"{Gear}")
            self.ViewDataStorageM_Comparison.gear = self.ViewDataStorageM.gear


    def Drs(self):
        if self.ViewDataStorageM.drs != self.ViewDataStorageM_Comparison.drs:
            if self.ViewDataStorageM.drs:
                self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(0, 255, 0);")
            self.ViewDataStorageM_Comparison.drs = self.ViewDataStorageM.drs

    def PacketCarStatusData(self):
        self.Drs_Available()

        if self.ViewDataStorageM.ersDeployMode != self.ViewDataStorageM_Comparison.ersDeployMode:
            ersDeployMode_text = {0: "None", 1: "Medium", 2: "HotLap", 3: "Overtake"}
            ersDeployMode_num = self.ViewDataStorageM.ersDeployMode
            self.Set_Text.emit("RES_Mode", F"{ersDeployMode_text[ersDeployMode_num]}")
            self.ViewDataStorageM_Comparison.ersDeployMode = self.ViewDataStorageM.ersDeployMode

        if self.ViewDataStorageM.ersStore != self.ViewDataStorageM_Comparison.ersStore:
            self.ImageP.ERS_Store_Fill(self.ViewDataStorageM.ersStore)
            self.Set_Pixmap.emit("ERS_Store", self.ImageP.ERS_Store_GetImg())
            self.ViewDataStorageM_Comparison.ersStore = self.ViewDataStorageM.ersStore

        if self.ViewDataStorageM.ersDeployed != self.ViewDataStorageM_Comparison.ersDeployed:
            self.ImageP.ERS_Deploted_Fill(self.ViewDataStorageM.ersDeployed)
            self.Set_Pixmap.emit("ERS_Deploted", self.ImageP.ERS_Deploted_GetImg())
            self.ViewDataStorageM_Comparison.ersDeployed = self.ViewDataStorageM.ersDeployed


    def Drs_Available(self):
        if self.ViewDataStorageM.drsAllowed != self.ViewDataStorageM_Comparison.drsAllowed or self.ViewDataStorageM.drs != self.ViewDataStorageM_Comparison.drs:
            drs_allowed = self.ViewDataStorageM.drsAllowed
            drs = self.ViewDataStorageM.drs
            if (not drs) and (drs_allowed == 1):
                self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(255, 0, 0);")
            elif (not drs) and (drs_allowed == 0):
                self.Set_StyleSheet.emit("DRSLED", "color: rgb(255, 255, 255);background-color: rgb(0, 0, 0);")
            self.ViewDataStorageM_Comparison.drsAllowed = self.ViewDataStorageM.drsAllowed

    def PacketFinalClassificationData(self):
        pass

    def PacketCarDamageData(self):
        if self.ViewDataStorageM.tireDamage != self.ViewDataStorageM_Comparison.tireDamage:
            for i, data in enumerate(self.ViewDataStorageM.tireDamage):
                self.Set_Text.emit(F"tyresWear_{i + 1}_Text", F"{int(data)}%")
            self.ViewDataStorageM_Comparison.tireDamage = self.ViewDataStorageM.tireDamage


