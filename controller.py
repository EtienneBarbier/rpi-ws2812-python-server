import conf
from lib import *
import argparse
import signal
import shared
import sys
import threading
import led_strip_conf as lsc
from annimation_rainbow_list import *
from utils_controller import *

try:
    import neopixel as np
except ImportError:
    import fake_neopixel as np # If we don't are under raspberry than set debuf true
    conf.debug_cont = 1;

conf.init_led_table(lsc.list[0]["count"],lsc.list[1]["count"]);

class Controller():

    def __init__(self,event_end_start):
        self._event_end_start = event_end_start
        self._strip1 = np.Adafruit_NeoPixel(lsc.list[0]["count"], lsc.list[0]["pin"], lsc.conf["freq"], lsc.conf["freq"], lsc.list[0]["invert"], lsc.list[0]["brighness"], lsc.list[0]["channel"])
        self._strip2 = np.Adafruit_NeoPixel(lsc.list[1]["count"], lsc.list[1]["pin"], lsc.conf["freq"], lsc.conf["freq"], lsc.list[1]["invert"], lsc.list[1]["brighness"], lsc.list[1]["channel"])
        self._strip1.begin()
        self._strip2.begin()

    def setBrightness(self,brighness):
        self._strip1.setBrightness(int(255*brighness));
        self._strip2.setBrightness(int(255*brighness));
        self._strip1.show();
        self._strip2.show();

    def _fixedColor(self):
        if conf.debug_cont:
            debug("Set Color "+ str(shared.color[0]) + " " + str(shared.color[1])+ " " + str(shared.color[2]))
        setColor(self,shared.color);
        infinitedelay(self)


    def run(self):
        if conf.debug_cont:
            print('#### Start LEDS controller ####')
        while True:
            if shared.restart:
                self._event_end_start.clear()
                shared.restart = False
                shared.start = True

            while not shared.start:
                setColor(self,[0,0,0]);
                self._event_end_start.wait()
            self._event_end_start.clear()


            while shared.start:
                try:
                    myfunc = None
                    if (shared.current == "fixed_color"):
                         self._fixedColor()
                    else:
                        for i in range(len(annimation_list)):
                            if annimation_list[i]["id"] == shared.current:
                                myfunc = annimation_list[i]["function"];
                        if myfunc != None:
                            myfunc(self);
                        else:
                            setColor(self,[255,0,0]);
                except EndAnimException:
                    if conf.debug_cont:
                        conf.init_led_table(LED_1_COUNT, LED_2_COUNT);
                        print("Stop Animation")
                    pass

                self._event_end_start.wait(timeout=0)
            self._event_end_start.clear()
