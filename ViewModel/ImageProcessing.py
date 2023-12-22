import cv2
import numpy as np

from PyQt5.QtGui import QImage

class BarImg:
    def __init__(self, size):
        self.size = size
        self.__img = np.full((self.size[0], self.size[1], 3), (255, 255, 0), dtype=np.uint8)

    @property
    def img(self):
        return QImage(self.__img, self.size[0], self.size[1], (self.size[0]*self.size[1]) * 3, QImage.Format_RGB888)

class ImageProcessing:
    def __init__(self):
        self.RPMBar_init()

    def RPMBar_init(self):
        self.RPMBar = BarImg([464, 41])


    def ERS_Store_init(self):
        self.ERS_Store = BarImg([182, 35])

    def ERS_Deploted_init(self):
        self.ERS_Deploted = BarImg([182, 35])


    def RPMBar_GetImg(self):
        return self.RPMBar.img