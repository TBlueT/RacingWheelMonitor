from PyQt5 import QtCore, QtGui, QtTest

from ViewModel import ImageProcessing

class DisplayManagementViewModel(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)
    Set_Pixmap = QtCore.pyqtSignal(str, QtGui.QPixmap)
    Set_StyleSheet = QtCore.pyqtSignal(str, str)
    Set_page = QtCore.pyqtSignal(int)

    def __init__(self):
        super(DisplayManagementViewModel, self).__init__()

        self.ImageP = ImageProcessing()

    def run(self):
        while True:
            self.Set_Pixmap.connect("RPMBar", self.ImageP.RPMBar_GetImg())