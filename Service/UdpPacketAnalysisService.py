import socket, time

from PyQt5 import QtCore, QtGui, QtTest

from Model import *

class UdpPacketAnalysisService(QtCore.QThread):

    def __init__(self, parent=None):
        super(UdpPacketAnalysisService, self).__init__()

        self.DisplayManagement_VM = parent.DisplayManagement_VM

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.f1_22_pi_ip = str(s.getsockname()[0])
        s.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 20777))
        self.sock.settimeout(0.5)

    def run(self):
        while True:
            buf = []
            try:
                data, addr = self.sock.recvfrom(1500)
                buf = unpack_udp_packet(data)
            except:
                pass

            if buf:
                if buf.header.packetId == 7:
                    self.DisplayManagement_VM.ImageP.RPMBar_setMaxRpm(int(buf.carStatusData[buf.header.playerCarIndex].maxRPM))
                    #print(buf.carStatusData[buf.header.playerCarIndex].maxRPM)
                elif buf.header.packetId == 6:
                    self.DisplayManagement_VM.ImageP.RPMBar_RpmFill(int(buf.carTelemetryData[buf.header.playerCarIndex].engineRPM))