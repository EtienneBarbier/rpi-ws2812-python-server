import annimation_rainbow_function as liban

def init():
    global controller
    global brightness
    global speed
    global start
    global restart
    global current
    global color
    global locked_timeout

    brightness = 1
    speed = 1
    start = False
    restart = False
    current = "fixed_color"
    color = [255,255,255]
    locked_timeout = False
