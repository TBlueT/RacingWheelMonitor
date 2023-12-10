import threading, time


class Console(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.__PrintWaitiong:list[str] = []

        self.__printTimeSet = 0.01
        self.__printTime = time.time()

    @property
    def PrintWaitiong(self):
        return self.__PrintWaitiong.pop(0)

    @PrintWaitiong.setter
    def PrintWaitiong(self, strdata:str):
        self.__PrintWaitiong.append(strdata)


    def run(self):
        while True:
            temp_time = time.time()
            if temp_time - self.__printTime > self.__printTimeSet:
                if self.__PrintWaitiong != []:
                    print(self.PrintWaitiong)

                self.__printTime = temp_time
            time.sleep(0.008)