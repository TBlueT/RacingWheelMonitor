import cv2
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

class BarImg:
    def __init__(self, size):
        self.size = size
        self.__img = np.full((self.size[1], self.size[0], 3), (100, 100, 0), dtype=np.uint8)

    @property
    def img(self):
        h, w, c = self.__img.shape
        return QPixmap.fromImage(QImage(self.__img,  w, h, w*c, QImage.Format_RGB888))

    def Graduation_init(self):
        temp_xPoint = int(self.size[0]/10)
        temp_yPoint = int(self.size[1]/6)

        for i in range(1, 10):
            start_point_1 = (temp_xPoint*i, 0)
            end_point_1 = (temp_xPoint*i, temp_yPoint)
            start_point_2 = (temp_xPoint*i, temp_yPoint * 5)
            end_point_2 = (temp_xPoint*i, self.size[1])
            self.__img = cv2.line(self.__img, start_point_1, end_point_1, (74, 74, 74), 2)
            cv2.putText(self.__img, F"{i}", (temp_xPoint*i-5, int(temp_yPoint*4.23)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (74,74,74), 2, cv2.LINE_AA)
            self.__img = cv2.line(self.__img, start_point_2, end_point_2, (74, 74, 74), 2)



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