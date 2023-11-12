import socket
import shutil
import os

from ViewModel import *

DisplayVM = DisplayViewModel()

ipaddress=socket.gethostbyname(socket.gethostname())
if ipaddress=="127.0.0.1":
    print("You are not connected to the internet!")
else:
    if os.path.isdir('RacingWheelDashboard'):
        shutil.rmtree('RacingWheelDashboard')
    os.system('git clone https://github.com/TBlueT/RacingWheelDashboard.git')
