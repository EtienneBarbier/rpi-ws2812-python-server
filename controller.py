import time
import conf
import argparse
import signal
import sys
import threading
from utils_controller import *

try:
    import neopixel as np
except ImportError:
    import fake_neopixel as np
    import fake_ws as ws

# LED strip configuration:
LED_1_COUNT      = 42      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
LED_1_STRIP      = ws.WS2811_STRIP_GRB

LED_2_COUNT      = 42      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = ws.WS2811_STRIP_GRB


class Controller():

    def __init__(self,event_end_start):
        self.event_end_start = event_end_start
        self.strip1 = np.Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
        self.strip2 = np.Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)
        self.strip1.begin()
        self.strip2.begin()


#        threading.Thread.__init__(self)

    def reset(self):
        print("Reset LEDS")

    def rainbow(self):
        for j in range(256):
            for i in range(LED_1_COUNT):
                self.strip1.setPixelColor(i, wheel((i+j) & 255))
                self.strip2.setPixelColor(i, wheel((i+j) & 255))
            self.strip1.show()
            self.strip2.show()
            self.event_end_start.wait(timeout=0.02)
            if(self.event_end_start.is_set()):
                break

    def rainbowCycle(self):
        for j in range(256):
            for i in range(LED_1_COUNT):
                self.strip1.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
                self.strip2.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
            self.strip1.show()
            self.strip2.show()
            self.event_end_start.wait(timeout=0.02)
            if(self.event_end_start.is_set()):
                break

    def theaterChaseRainbow(self):
        for j in range(256):
            for q in range(3):
                for i in range(0, LED_1_COUNT, 3):
                    self.strip1.setPixelColor(i+q, wheel((i+j) % 255))
                    self.strip2.setPixelColor(i+q, wheel((i+j) % 255))
                self.strip1.show()
                self.strip2.show()
                self.event_end_start.wait(timeout=0.05)
                if self.event_end_start.is_set():
                    break
                for i in range(0, LED_1_COUNT, 3):
                    self.strip1.setPixelColor(i+q, 0)
                    self.strip2.setPixelColor(i+q, 0)

    def fixedColor(self):
        for i in range(LED_1_COUNT):
            self.strip1.setPixelColor(Color(conf.color[0,conf.color[1],conf.color[2]]))
            self.strip2.setPixelColor(Color(conf.color[0,conf.color[1],conf.color[2]]))
        self.strip1.show()
        self.strip2.show()
        self.event_end_start.wait()

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
                elif (conf.current == "FIXED_COLOR"):
                    self.fixedColor()
                else:
                    self.rainbow()
                    self.rainbowCycle()
                    self.theaterChaseRainbow()

                self.event_end_start.wait(timeout=2)
            self.event_end_start.clear()

            print("Out of loop")
