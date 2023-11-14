import threading, time, pyautogui


class PreventScreenFromTurningOff(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            pyautogui.click()
            time.sleep(180)