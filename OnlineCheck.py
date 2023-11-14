from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic

import socket, shutil, os, sys, time


GUI_class = uic.loadUiType('/home/pi/Preliminaries.ui')[0]
class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showFullScreen()


        self.SetText("label", "Checking wifi connection...")

        ipaddress = socket.gethostbyname(socket.gethostname())
        if ipaddress == "127.0.0.1":
            self.SetText("label", "You are not\n connected to the internet!")
        else:
            self.SetText("label", "Internet connected")
            time.sleep(1)
            self.SetText("label", "Download the latest file...")
            time.sleep(1)
            if os.path.isdir('RacingWheelDashboard'):
                shutil.rmtree('RacingWheelDashboard')
            self.SetText("label", os.popen('git clone https://github.com/TBlueT/RacingWheelDashboard.git').read())

    def SetText(self, id:str="", string:str=""):
        if id:
            getattr(self, id).setText(string)
        else:
            pass

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


