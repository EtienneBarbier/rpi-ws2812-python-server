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
    current = "FIXED_COLOR"
    color = [255,255,255]
    locked_timeout = False
