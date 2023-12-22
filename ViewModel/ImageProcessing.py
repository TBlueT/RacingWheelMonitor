import cv2
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

class BarImg:
    def __init__(self, size):
        self.size = size
        self.__img = np.full((self.size[0], self.size[1], 3), (100, 100, 0), dtype=np.uint8)

    @property
    def img(self):
        return QPixmap.fromImage(QImage(self.__img, self.size[0], self.size[1], self.size[0]*3, QImage.Format_RGB888))

    def Graduation_init(self):
        temp_xPoint = int(self.size[0]/10)
        temp_yPoint = self.size[1]
        start_point = (temp_xPoint, 0)
        end_point = (temp_xPoint, temp_yPoint)
        self.__img = cv2.line(self.__img, start_point, end_point, (0,255,0), 5)

class ImageProcessing:
    def __init__(self, parent=None):
        self.mainUi = parent
        self.RPMBar_init()
        self.ERS_Store_init()
        self.ERS_Deploted_init()

    def RPMBar_init(self):
        self.RPMBar = BarImg([self.mainUi.RPMBar.size().width(),self.mainUi.RPMBar.size().height()])
        self.RPMBar.Graduation_init()

    def ERS_Store_init(self):
        self.ERS_Store = BarImg([self.mainUi.ERS_Store.size().width(),self.mainUi.ERS_Store.size().height()])

    def ERS_Deploted_init(self):
        self.ERS_Deploted = BarImg([self.mainUi.ERS_Deploted.size().width(),self.mainUi.ERS_Deploted.size().height()])


    def RPMBar_GetImg(self):
        return self.RPMBar.img
    def ERS_Store_GetImg(self):
        return self.ERS_Store.img
    def ERS_Deploted_GetImg(self):
        return self.ERS_Deploted.img