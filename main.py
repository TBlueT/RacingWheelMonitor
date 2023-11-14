from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys


GUI_class = uic.loadUiType('/home/pi/RacingWheelMonitor/View/pi_ui.ui')[0]
class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showFullScreen()
        #self.show()



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


