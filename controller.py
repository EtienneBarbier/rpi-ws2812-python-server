import time
import conf
import threading


class Controller():

    def __init__(self,event_inter):
        self.event_inter = event_inter

#        threading.Thread.__init__(self)

    def reset(self):
        print("Reset LEDS")

    def run(self):
        print ('Start LEDS controller')
        while not self.event_inter.is_set():
            print(conf.brightness)
            self.event_inter.wait(timeout=2)

        self.event_inter.clear()
