import time
import conf
import threading
from utils_controller import *


class Controller():

    def __init__(self,event_inter):
        self.event_inter = event_inter

#        threading.Thread.__init__(self)

    def reset(self):
        print("Reset LEDS")

    def rainbow(self):
        for j in range(256):
            for i in range(42):
                print(str(i) + "-" + str(wheel((i+j) & 255)))
            print("Display")
            self.event_inter.wait(timeout=0.2)
            if(self.event_inter.is_set()):
                break

    def run(self):
        print ('Start LEDS controller')
        while True:
            while not conf.start:
                self.event_inter.wait()
            self.event_inter.clear()


            while conf.start:
                print(conf.brightness)
                self.rainbow()
                self.event_inter.wait(timeout=2)
            self.event_inter.clear()

            print("Out of loop")
