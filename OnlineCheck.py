from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import socket, shutil, os, sys, time, threading


GUI_class = uic.loadUiType('/home/pi/Preliminaries.ui')[0]
class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showFullScreen()
        #self.show()

        self.AP = AdvancePreparation(self)
        self.AP.start()

    def SetText(self, id:str="", string:str=""):
        if id:
            getattr(self, id).setText(string)
        else:
            pass

class AdvancePreparation(threading.Thread):
    def __init__(self, parents:object = None):
        threading.Thread.__init__(self)
        self.main = parents

    def run(self):
        time.sleep(1)
        self.main.SetText("label", "Checking wifi connection...")
        time.sleep(1)
        ipaddress = socket.gethostbyname(socket.gethostname())
        if ipaddress == "127.0.0.1":
            self.main.SetText("label", "You are not\n connected to the internet!")
        else:
            self.main.SetText("label", "Internet connected")
            time.sleep(1)
            self.main.SetText("label", "Download the latest file...")
            time.sleep(1)
            if os.path.isdir('RacingWheelMonitor'):
                shutil.rmtree('RacingWheelMonitor')
            os.system('git clone https://github.com/TBlueT/RacingWheelMonitor.git')
            self.main.SetText("label", "Download completed and run...")
            os.popen('python3 /home/pi/RacingWheelMonitor/main.py')


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


