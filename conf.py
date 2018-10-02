def init():
    global debug_cont # Debug for controller part (led)
    debug_cont = 0
    global debug_serv # Debug for server part (web server)
    debug_serv = 0
    global brightness
    brightness = 1
    global speed
    speed = 1
    global start
    start = False
    global restart
    restart = False
    global current
    current = "RAINBOW"
    global color
    color = [255,255,255]
    global locked_timeout
    locked_timeout = False
