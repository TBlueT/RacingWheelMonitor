import socket, time

from PyQt5 import QtCore, QtGui, QtTest

from Model import *

class UdpPacketAnalysisService(QtCore.QThread):

    def __init__(self):
        super(UdpPacketAnalysisService, self).__init__()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.f1_22_pi_ip = str(s.getsockname()[0])
        s.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 8282))
        self.sock.settimeout(0.5)

    def run(self):
        while True:
            buf = []
            try:
                data, addr = self.sock.recvfrom(1500)
                buf = unpack_udp_packet(data)
            except:
                pass
