import socket, time, datetime

from PyQt5 import QtCore, QtGui, QtTest

from Model import *

class UdpPacketAnalysisService(QtCore.QThread):

    def __init__(self, parent=None):
        super(UdpPacketAnalysisService, self).__init__()

        self.ViewDataStorageM = parent.ViewDataStorageM

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ViewDataStorageM.f1_24_pi_ip = str(s.getsockname()[0])
        s.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 20777))
        self.sock.settimeout(0.5)

        self.ck_game_start: bool = False
        self.ck_game_udp_time = time.time()
        self.ck_game_udp_out_time: int = 5

    def run(self):
        while True:
            buf = []
            try:
                data, addr = self.sock.recvfrom(1500)
                buf = unpack_udp_packet(data)
            except:
                pass

            if buf:
                if self.ViewDataStorageM.f1_24_pi_ip_bool:
                    self.ViewDataStorageM.f1_24_pi_ip_bool = False

                if buf.header.packetId == 1:
                    self.ViewDataStorageM.lapAll = int(buf.totalLaps)

                elif buf.header.packetId == 2:
                    self.ViewDataStorageM.lap = int(buf.lapData[buf.header.playerCarIndex].currentLapNum)
                    self.ViewDataStorageM.lapTime = int(buf.lapData[buf.header.playerCarIndex].currentLapTime)

                elif buf.header.packetId == 7:
                    self.ViewDataStorageM.drsAllowed = int(buf.carStatusData[buf.header.playerCarIndex].drsAllowed)
                    self.ViewDataStorageM.maxRpm = int(buf.carStatusData[buf.header.playerCarIndex].maxRPM)
                    self.ViewDataStorageM.ersStore = buf.carStatusData[buf.header.playerCarIndex].ersStoreEnergy
                    self.ViewDataStorageM.ersDeployed = buf.carStatusData[buf.header.playerCarIndex].ersDeployedThisLap
                    self.ViewDataStorageM.ersDeployMode = int(buf.carStatusData[buf.header.playerCarIndex].ersDeployMode)

                elif buf.header.packetId == 6:
                    self.ViewDataStorageM.speed = int(buf.carTelemetryData[buf.header.playerCarIndex].speed)
                    self.ViewDataStorageM.gear = int(buf.carTelemetryData[buf.header.playerCarIndex].gear)
                    self.ViewDataStorageM.rpm = int(buf.carTelemetryData[buf.header.playerCarIndex].engineRPM)
                    self.ViewDataStorageM.drs = int(buf.carTelemetryData[buf.header.playerCarIndex].drs)
                    self.ViewDataStorageM.tireTemperature = [int(buf.carTelemetryData[buf.header.playerCarIndex].tyresSurfaceTemperature[0]),
                                                             int(buf.carTelemetryData[buf.header.playerCarIndex].tyresSurfaceTemperature[1]),
                                                             int(buf.carTelemetryData[buf.header.playerCarIndex].tyresSurfaceTemperature[2]),
                                                             int(buf.carTelemetryData[buf.header.playerCarIndex].tyresSurfaceTemperature[3])
                                                             ]

                elif buf.header.packetId == 10:
                    self.ViewDataStorageM.tireDamage = [int(buf.CarDamageData[buf.header.playerCarIndex].tyresWear[0]),
                                                        int(buf.CarDamageData[buf.header.playerCarIndex].tyresWear[1]),
                                                        int(buf.CarDamageData[buf.header.playerCarIndex].tyresWear[2]),
                                                        int(buf.CarDamageData[buf.header.playerCarIndex].tyresWear[3]),
                                                        ]
            else:
                if time.time() - self.ck_game_udp_time > self.ck_game_udp_out_time:
                    self.ViewDataStorageM.f1_24_pi_ip_bool = True
                    self.ck_game_udp_time = time.time()