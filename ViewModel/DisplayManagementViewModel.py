import time

from PyQt5 import QtCore, QtGui, QtTest

from ViewModel.ImageProcessing import ImageProcessing

class DisplayManagementViewModel(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)
    Set_Pixmap = QtCore.pyqtSignal(str, QtGui.QPixmap)
    Set_StyleSheet = QtCore.pyqtSignal(str, str)
    Set_page = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(DisplayManagementViewModel, self).__init__()

        self.ViewDataStorageM = parent.ViewDataStorageM
        self.ImageP = ImageProcessing(parent)

    # def RPMBar_SetMaxRPM(self, maxRpm:int):
    #     self.ImageP.
        self.DisplayUpdateTimeSet = 0.05
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
        pass

    def PacketCarTelemetryData(self):
        self.ImageP.RPMBar_RpmFill(self.ViewDataStorageM.rpm)
        self.Set_Text.emit("RPMText", F"{self.ViewDataStorageM.rpm}")
        self.Set_Pixmap.emit("RPMBar", self.ImageP.RPMBar_GetImg())

    def PacketCarStatusData(self):
        self.Set_Pixmap.emit("ERS_Store", self.ImageP.ERS_Store_GetImg())
        self.Set_Pixmap.emit("ERS_Deploted", self.ImageP.ERS_Deploted_GetImg())

    def PacketFinalClassificationData(self):
        pass

    def PacketCarDamageData(self):
        pass
