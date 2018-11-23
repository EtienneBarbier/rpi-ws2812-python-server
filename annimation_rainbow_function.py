import led_strip_conf as lsc
import conf
import random
from utils_controller import *

LED_1_COUNT = lsc.list[0]["count"];
LED_2_COUNT = lsc.list[1]["count"];

def rainbowRandom(self):
    if conf.debug_cont:
        debug("Set rainbowRandom")
    conf.led_1_tab[random_led(LED_1_COUNT)] = random_color_tab(100);
    conf.led_2_tab[random_led(LED_2_COUNT)] = random_color_tab(100);
    for i in range(LED_1_COUNT):
        color1 = compute_color_tab(conf.led_1_tab[i]);
        color2 = compute_color_tab(conf.led_2_tab[i]);
        self._strip1.setPixelColor(i,color1);
        self._strip2.setPixelColor(i,color2);
        if conf.led_1_tab[i][0] > 0:
            conf.led_1_tab[i] = reduce_lightness_tab(conf.led_1_tab[i],2);
        if conf.led_2_tab[i][0] > 0:
            conf.led_2_tab[i] = reduce_lightness_tab(conf.led_2_tab[i],2);
    self._strip1.show()
    self._strip2.show()
    delay(self,timeout=0.2)


def rainbow(self):
    if conf.debug_cont:
        debug("Set rainbow")
    for j in range(256):
        for i in range(LED_1_COUNT):
            self._strip1.setPixelColor(i, wheel((i+j) & 255))
            self._strip2.setPixelColor(i, wheel((i+j) & 255))
        self._strip1.show()
        self._strip2.show()
        delay(self,timeout=0.02)

def rainbowCycle(self):
    if conf.debug_cont:
        debug("Set rainbowCycle")
    for j in range(256):
        for i in range(LED_1_COUNT):
            self._strip1.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
            self._strip2.setPixelColor(i, wheel((int(i * 256 / LED_1_COUNT) + j) & 255))
        self._strip1.show()
        self._strip2.show()
        delay(self,timeout=0.02)

def theaterChaseRainbow(self):
    if conf.debug_cont:
        debug("Set theaterChaseRainbow")
    for j in range(256):
        for q in range(3):
            for i in range(0, LED_1_COUNT, 3):
                self._strip1.setPixelColor(i+q, wheel((i+j) % 255))
                self._strip2.setPixelColor(i+q, wheel((i+j) % 255))
            self._strip1.show()
            self._strip2.show()
            delay(self,timeout=0.05)
            for i in range(0, LED_1_COUNT, 3):
                self._strip1.setPixelColor(i+q, 0)
                self._strip2.setPixelColor(i+q, 0)
                nodelay(self)
