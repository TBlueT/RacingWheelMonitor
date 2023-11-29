from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import socket, shutil, os, sys, time, threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

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
            time.sleep(1)
            self.main.SetText("label", "Connect to WiFi\n WiFi name: RacingWheeM\n password: 12345678")
        else:
            self.main.SetText("label", "Internet connected")
            time.sleep(1)
            self.main.SetText("label", "Download the latest file...")
            time.sleep(1)
            if os.path.isdir('RacingWheelMonitor'):
                os.system("cp -r -f /home/pi/RacingWheelMonitor /home/pi/RacingWheelMonitor_BUp")
                shutil.rmtree('RacingWheelMonitor')
            os.system('git clone https://github.com/TBlueT/RacingWheelMonitor.git')
            self.main.SetText("label", "Download completed and run...")
            os.system('python3 /home/pi/RacingWheelMonitor/main.py')

            self.main.SetText("label", "Download failed\n backup file restoration...")
            os.system("cp -r -f /home/pi/RacingWheelMonitor_BUp /home/pi/RacingWheelMonitor")
            os.system('python3 /home/pi/RacingWheelMonitor_BUp/main.py')

#https://with-rl.tistory.com/entry/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-APAccess-Point%EB%A1%9C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        temp_query = urlparse(self.path).query
        if temp_query:
            temp_wifi = ["",""]
            for i, data in enumerate(temp_query.split("&")):
                temp_wifi[i] = data.split("=")[1]
            print(temp_wifi)
            text1 = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
            text1 += "update_config=1\n\n"
            text1 += "network={\n"
            text1 += F'        ssid="{temp_wifi[0]}"\n'
            text1 += F'        psk="{temp_wifi[1]}"\n'
            text1 += "}"

            file = open("wpa_supplicant.conf", "w")
            file.write(text1)
            file.close()


        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<!DOCTYPE html>'.encode('utf-8'))
            self.wfile.write('<html>'.encode('utf-8'))
            self.wfile.write('<body>'.encode('utf-8'))
            self.wfile.write('<h2>Wifi 연결</h2>'.encode('utf-8'))
            self.wfile.write('<form action="/wifiConnection" method="get">'.encode('utf-8'))
            self.wfile.write('<label for="wifiname">Wifi 이름:</label><br>'.encode('utf-8'))
            self.wfile.write('<input type="text" id="wifiname" name="wifiname"><br>'.encode('utf-8'))
            self.wfile.write('<label for="wifipassword">Wifi 비밀번호:</label><br>'.encode('utf-8'))
            self.wfile.write('<input type="password" id="wifipassword" name="wifipassword">'.encode('utf-8'))
            self.wfile.write('<br><br>'.encode('utf-8'))
            self.wfile.write('<input type="submit" value="Wifi 연결하기">'.encode('utf-8'))
            self.wfile.write('</form> '.encode('utf-8'))
            self.wfile.write('</body>'.encode('utf-8'))
            self.wfile.write('</html>'.encode('utf-8'))

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


