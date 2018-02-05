import time
import conf
#from neopixel import *
import argparse
import signal
import sys

import threading
from utils_controller import *


# LED strip configuration:
LED_COUNT      = 66     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering




class Controller():

    def __init__(self,event_end_start):
        self.event_end_start = event_end_start

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.strip.begin()


#        threading.Thread.__init__(self)

    def reset(self):
        print("Reset LEDS")

    def rainbow(self):
        for j in range(256):
            for i in range(LED_COUNT):
                #print(str(i) + "-" + str(wheel((i+j) & 255)))
                #self.strip.setPixelColor(i, wheel((i+j) & 255))
            #self.strip.show()
            self.event_end_start.wait(timeout=0.02)
            if(self.event_end_start.is_set()):
                break

    def rainbowCycle(self):
        for j in range(256):
            for i in range(LED_COUNT):
                #self.strip.setPixelColor(i, wheel((int(i * 256 / LED_COUNT) + j) & 255))
            #self.strip.show()
            self.event_end_start.wait(timeout=0.02)
            if(self.event_end_start.is_set()):
                break

    def theaterChaseRainbow(self):
        for j in range(256):
            for q in range(3):
                for i in range(0, LED_COUNT, 3):
                    #self.strip.setPixelColor(i+q, wheel((i+j) % 255))
                #self.strip.show()
                self.event_end_start.wait(timeout=0.05)
                if(self.event_end_start.is_set()):
                    break
                for i in range(0, LED_COUNT, 3):
                    #self.strip.setPixelColor(i+q, 0)

    def run(self):
        print ('Start LEDS controller')
        while True:
            if conf.restart:
                self.event_end_start.clear()
                conf.restart = False
                conf.start = True

            while not conf.start:
                self.event_end_start.wait()
            self.event_end_start.clear()


            while conf.start:
                if(conf.current == "RAINBOW"):
                    self.rainbow()
                elif(conf.current == "RAINBOW_CYCLE"):
                    self.rainbowCycle()
                elif(conf.current == "THEATER_CHASE_RAINBOW"):
                    self.theaterChaseRainbow()
                else:
                    self.rainbow()
                    self.rainbowCycle()
                    self.theaterChaseRainbow()

                self.event_end_start.wait(timeout=2)
            self.event_end_start.clear()

            print("Out of loop")
