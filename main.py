from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys, os

from Service import *



GUI_class = uic.loadUiType('/home/pi/RacingWheelMonitor/View/pi_ui.ui')[0]
class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        os.system("cp -f /home/pi/RacingWheelMonitor/OnlineCheck.py /home/pi/OnlineCheck.py")

        self.console = Console()
        self.console.start()

        self.L = LedBr()  # LED bar output processing.
        self.data_process = Process(self)  # UDP data processing and various data processing.
        self.data_process.Set_Text.connect(self.Set_Text)
        self.data_process.Set_Pixmap.connect(self.Set_Pixmap)
        self.data_process.Set_StyleSheet.connect(self.Set_StyleSheet)
        self.data_process.Set_page.connect(self.Set_page)
        self.L.start()
        self.data_process.start()


        self.showFullScreen()
        #self.show()

    @pyqtSlot(str, str)
    def Set_Text(self, object, data):  # Text display data storage function.
        #self.lock.lock()
        getattr(self, object).setText(data)
        #self.lock.unlock()

    @pyqtSlot(str, QPixmap)
    def Set_Pixmap(self, object, data):  # Image display data storage function.
        #self.lock.lock()
        getattr(self, object).setPixmap(data)
        #self.lock.unlock()

    @pyqtSlot(str, str)
    def Set_StyleSheet(self, object, data):  # Stylesheet display data storage function.
        #self.lock.lock()
        getattr(self, object).setStyleSheet(data)
        #self.lock.unlock()

    @pyqtSlot(int)
    def Set_page(self, page):
        self.stackedWidget_4.setCurrentIndex(page)

    def Set_object_init(self):  # Clear display storage.
        self.setStyleSheet_Waiting = {}
        self.setText_Waiting = {}
        self.setPixmax_Waiting = {}

    def set_img_Go(self):  # Display screen update.
        # self.lock.lock()
        # self.setUpdatesEnabled(False)
        try:
            # if self.setText_Waiting != {}:
            #     for data in self.setText_Waiting:
            #         getattr(self, data).setText(self.setText_Waiting[data])
            # if self.setPixmax_Waiting != {}:
            #     for data in self.setPixmax_Waiting:
            #         getattr(self, data).setPixmap(self.setPixmax_Waiting[data])
            # if self.setStyleSheet_Waiting != {}:
            #     for data in self.setStyleSheet_Waiting:
            #         getattr(self, data).setStyleSheet(self.setStyleSheet_Waiting[data])
            #         time.sleep(0.05)
            pass

        except Exception as e:
            print(F"set img: {e}")

        self.Set_object_init()

    def closeEvent(self, evant):
        self.udp_pack.Working = False
        self.data_process.Working = False



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


