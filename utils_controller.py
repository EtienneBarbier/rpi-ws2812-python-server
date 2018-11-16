import random


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
