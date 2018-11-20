import time
import conf
from lib import *
import argparse
import signal
import sys
import threading
import random
from utils_controller import *

try:
    import neopixel as np
except ImportError:
    import fake_neopixel as np # If we don't are under raspberry than set debuf true
    conf.debug_cont = 1;

# LED strip configuration:
LED_1_COUNT      = 42      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
# LED_1_STRIP      = np.ws.WS2811_STRIP_GRB

LED_2_COUNT      = 42      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
# LED_2_STRIP      = np.ws.WS2811_STRIP_GRB

conf.init_led_table(LED_1_COUNT,LED_2_COUNT);


class EndAnimException(Exception):
    pass

def debug(message):
    print("Led : " + message)

class Controller():

    def __init__(self,event_end_start):
        self._event_end_start = event_end_start
        self._strip1 = np.Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL)
        self._strip2 = np.Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL)
        self._strip1.begin()
        self._strip2.begin()

    def setBrightness(self,brighness):
        self._strip1.setBrightness(int(255*brighness));
        self._strip2.setBrightness(int(255*brighness));
        self._strip1.show();
        self._strip2.show();

    def _infinitedelay(self):
        self._event_end_start.wait()
        if (self._event_end_start.is_set() and not shared.locked_timeout):
            raise EndAnimException
        else:
            self._event_end_start.clear()
            shared.locked_timeout = False;

    def _change_delay(self, timeout, first_timeout):
        start = time.time()
        self._event_end_start.wait(timeout=timeout)
        if (self._event_end_start.is_set() and not shared.locked_timeout):
            raise EndAnimException
        elif shared.locked_timeout:
            stop = time.time()
            remind = timeout - (stop - start)
            self._event_end_start.clear()
            shared.locked_timeout = False;
            new_time = (shared.speed * first_timeout)-(remind);
            if new_time >= 0:
                self._change_delay(new_time, first_timeout)

    def _delay(self, timeout):
        if shared.speed == -1:
            self._infinitedelay();
        else:
            tmp_timeout = shared.speed * timeout;
            self._change_delay(tmp_timeout,0);


    def _nodelay(self):
        if (self._event_end_start.is_set()):
            raise EndAnimException

    def reset(self):
        if conf.debug_cont:
            debug("Reset LEDS")

    def _rainbowRandom(self):
        if conf.debug_cont:
            debug("Set rainbowRandom")
        conf.led_1_tab[random_led(LED_1_COUNT)] = random_color_tab(100);
        conf.led_2_tab[random_led(LED_2_COUNT)] = random_color_tab(100);
        print(conf.led_2_tab)
        for i in range(LED_1_COUNT):
            color1 = compute_color_tab(conf.led_1_tab[i]);
            color2 = compute_color_tab(conf.led_2_tab[i]);
            self._strip1.setPixelColor(i,color1);
            self._strip2.setPixelColor(i,color2);
            self._strip1.show()
            self._strip2.show()
            if conf.led_1_tab[i][0] > 0:
                conf.led_1_tab[i] = reduce_lightness_tab(conf.led_1_tab[i],10);
            if conf.led_2_tab[i][0] > 0:
                conf.led_2_tab[i] = reduce_lightness_tab(conf.led_2_tab[i],10);
        self._delay(timeout=0.5)


    def _rainbow(self):
        if conf.debug_cont:
            debug("Set rainbow")
        for j in range(256):
            for i in range(LED_1_COUNT):
                self._strip1.setPixelColor(i, wheel((i+j) & 255))
                self._strip2.setPixelColor(i, wheel((i+j) & 255))
            self._strip1.show()
            self._strip2.show()
            self._delay(timeout=0.02)

    def _rainbowCycle(self):
        if conf.debug_cont:
            debug("Set rainbowCycle")
        for j in range(256):
            for i in range(LED_1_COUNT):
                self._strip1.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
                self._strip2.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
            self._strip1.show()
            self._strip2.show()
            self._delay(timeout=0.02)

    def _theaterChaseRainbow(self):
        if conf.debug_cont:
            debug("Set theaterChaseRainbow")
        for j in range(256):
            for q in range(3):
                for i in range(0, LED_1_COUNT, 3):
                    self._strip1.setPixelColor(i+q, wheel((i+j) % 255))
                    self._strip2.setPixelColor(i+q, wheel((i+j) % 255))
                self._strip1.show()
                self._strip2.show()
                self._delay(timeout=0.05)
                for i in range(0, LED_1_COUNT, 3):
                    self._strip1.setPixelColor(i+q, 0)
                    self._strip2.setPixelColor(i+q, 0)
                    self._nodelay()

    def _setColor(self,color):
        for i in range(LED_1_COUNT):
            self._strip1.setPixelColor(i,Color(color[0],color[1],color[2]))
            self._strip2.setPixelColor(i,Color(color[0],color[1],color[2]))
        self._strip1.show()
        self._strip2.show()

    def _fixedColor(self):
        if conf.debug_cont:
            debug("Set Color "+ str(shared.color[0]) + " " + str(shared.color[1])+ " " + str(shared.color[2]))
        self._setColor(shared.color);
        self._infinitedelay()


    def run(self):
        if conf.debug_cont:
            print('#### Start LEDS controller ####')
        while True:
            if shared.restart:
                self._event_end_start.clear()
                shared.restart = False
                shared.start = True

            while not shared.start:
                self._setColor([0,0,0]);
                self._event_end_start.wait()
            self._event_end_start.clear()


            while shared.start:
                try:
                    if(shared.current == "RAINBOW"):
                        self._rainbow()
                    elif(shared.current == "RAINBOW_CYCLE"):
                        self._rainbowCycle()
                    elif(shared.current == "THEATER_CHASE_RAINBOW"):
                        self._theaterChaseRainbow()
                    elif (shared.current == "FIXED_COLOR"):
                        self._fixedColor()
                    elif (shared.current == "RAINBOW_RANDOM"):
                        self._rainbowRandom()
                    else:
                        self._rainbow()
                        self._rainbowCycle()
                        self._theaterChaseRainbow()
                except EndAnimException:
                    if conf.debug_cont:
                        conf.init_led_table(LED_1_COUNT, LED_2_COUNT);
                        print("Stop Animation")
                    pass

                self._event_end_start.wait(timeout=0)
            self._event_end_start.clear()
