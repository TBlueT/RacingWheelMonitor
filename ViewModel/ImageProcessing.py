import cv2
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

class BarImg:
    def __init__(self, size):
        self.size = size
        self.__img = np.full((self.size[1], self.size[0], 3), (0, 0, 0), dtype=np.uint8)
        self.__img_bar = np.full((self.size[1], self.size[0], 3), (0, 0, 0), dtype=np.uint8)

    @property
    def img(self):
        temp_img = cv2.add(self.__img, self.__img_bar)
        h, w, c = temp_img.shape
        return QPixmap.fromImage(QImage(temp_img,  w, h, w*c, QImage.Format_RGB888))

    def graduation_init(self):
        self.maxRpm = 13
        temp_xPoint = int(self.size[0]/self.maxRpm)
        temp_yPoint = int(self.size[1]/6)

        temp_color = (100, 100, 100)

        for i in range(1, self.maxRpm):
            start_point_1 = (temp_xPoint*i, 0)
            end_point_1 = (temp_xPoint*i, temp_yPoint)
            start_point_2 = (temp_xPoint*i, temp_yPoint * 6)
            end_point_2 = (temp_xPoint*i, self.size[1])
            self.__img = cv2.line(self.__img, start_point_1, end_point_1, temp_color, 2)
            cv2.putText(self.__img, F"{i}", (temp_xPoint*i-(6+int(i/10)*4), int(temp_yPoint*4.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, temp_color, 2, cv2.LINE_AA)
            self.__img = cv2.line(self.__img, start_point_2, end_point_2, temp_color, 2)

    def setMaxbar(self, maxRpm):
        if self.maxRpm:
            if maxRpm!=0:
                self.maxRpm = maxRpm

    def barFill(self, fill:int):
        temp_barLength = int(self.size[0]/self.maxRpm*fill)

        start_point_1 = (0, 0)
        end_point_1 = (temp_barLength, int(self.size[1]))

        self.__img_bar = np.full((self.size[1], self.size[0], 3), (0, 0, 0), dtype=np.uint8)
        self.__img_bar = cv2.rectangle(self.__img_bar, start_point_1, end_point_1, (100, 100, 0), -1)



class ImageProcessing:
    def __init__(self, parent=None):
        self.mainUi = parent
        self.RPMBar_init()
        self.ERS_Store_init()
        self.ERS_Deploted_init()

    def RPMBar_init(self):
        self.RPMBar = BarImg([self.mainUi.RPMBar.size().width(),self.mainUi.RPMBar.size().height()])
        self.RPMBar.graduation_init()

    def RPMBar_setMaxRpm(self, maxRpm: int):
        if self.RPMBar:
            self.RPMBar.setMaxbar(maxRpm)

    def RPMBar_RpmFill(self, fill:int):
        if self.RPMBar:
            self.RPMBar.barFill(fill)

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