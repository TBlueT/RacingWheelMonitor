from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys, os

from Service import *
from ViewModel import *


GUI_class = uic.loadUiType('/home/pi/RacingWheelMonitor/View/RacingWheelMonitorView.ui')[0]
#GUI_class = uic.loadUiType('View/RacingWheelMonitorView.ui')[0]
class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        os.system("cp -f /home/pi/RacingWheelMonitor/OnlineCheck.py /home/pi/OnlineCheck.py")

        self.showFullScreen()
        #self.show()

        self.UdpPacketAnalysis_S = UdpPacketAnalysisService()

        self.DisplayManagement_VM = DisplayManagementViewModel(self)
        self.DisplayManagement_VM.Set_Text.connect(self.Set_Text)
        self.DisplayManagement_VM.Set_Pixmap.connect(self.Set_Pixmap)
        self.DisplayManagement_VM.Set_StyleSheet.connect(self.Set_StyleSheet)
        self.DisplayManagement_VM.Set_page.connect(self.Set_page)

        #print(self.RPMBar.size().width(), self.RPMBar.size().height())


        self.DisplayManagement_VM.start()

    @pyqtSlot(str, str)
    def Set_Text(self, object, data):  # Text display data storage function.
        getattr(self, object).setText(data)

    @pyqtSlot(str, QPixmap)
    def Set_Pixmap(self, object, data):  # Image display data storage function.
        getattr(self, object).setPixmap(data)

    @pyqtSlot(str, str)
    def Set_StyleSheet(self, object, data):  # Stylesheet display data storage function.
        getattr(self, object).setStyleSheet(data)

    @pyqtSlot(int)
    def Set_page(self, page):
        self.stackedWidget_4.setCurrentIndex(page)




def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)

    sys._excepthook(exctype, value, traceback)


if __name__ == "__main__":
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(mainWindow)
    MainWindow = mainWindow()
    app.exec()


