import random
import led_strip_conf as lsc
import shared
import time



class EndAnimException(Exception):
    pass

def debug(message):
    print("Led : " + message)

LED_1_COUNT = lsc.list[0]["count"];
LED_2_COUNT = lsc.list[1]["count"];

def setColor(ctrl,color):
    for i in range(LED_1_COUNT):
        ctrl._strip1.setPixelColor(i,Color(color[0],color[1],color[2]))
        ctrl._strip2.setPixelColor(i,Color(color[0],color[1],color[2]))
    ctrl._strip1.show()
    ctrl._strip2.show()

def Color(red, green, blue, white = 0):
	return (white << 24) | (red << 16)| (green << 8) | blue

def wheel(pos):
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def infinitedelay(ctrl):
    ctrl._event_end_start.wait()
    if (ctrl._event_end_start.is_set() and not shared.locked_timeout):
        raise EndAnimException
    else:
        ctrl._event_end_start.clear()
        shared.locked_timeout = False;

def change_delay(ctrl, timeout, first_timeout):
    start = time.time()
    ctrl._event_end_start.wait(timeout=timeout)
    if (ctrl._event_end_start.is_set() and not shared.locked_timeout):
        raise EndAnimException
    elif shared.locked_timeout:
        stop = time.time()
        remind = timeout - (stop - start)
        ctrl._event_end_start.clear()
        shared.locked_timeout = False;
        new_time = (shared.speed * first_timeout)-(remind);
        if new_time >= 0:
            change_delay(ctrl, new_time, first_timeout)

def delay(ctrl, timeout):
    if shared.speed == -1:
        infinitedelay(ctrl);
    else:
        tmp_timeout = shared.speed * timeout;
        change_delay(ctrl, tmp_timeout,0);


def nodelay(ctrl):
    if (ctrl._event_end_start.is_set()):
        raise EndAnimException

def random_led(nb_led):
	return random.randrange(0, nb_led-1)

def random_color_value():
	return random.randrange(0, 255);

def random_color_tab(default_light):
	return [default_light,random_color_value(),random_color_value(),random_color_value()];

def reduce_lightness_tab(tab, reduce_value):
	return [tab[0] - reduce_value,tab[1],tab[2],tab[3]]

def compute_color_tab(tab):
    return Color(int(tab[0]*tab[1]*0.01),int(tab[0]*tab[2]*0.01),int(tab[0]*tab[3]*0.01));
