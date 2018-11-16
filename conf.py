def init():
    global debug_cont # Debug for controller part (led)
    debug_cont = 0
    global debug_serv # Debug for server part (web server)
    debug_serv = 0

def init_led_table(nb_led_1,nb_led_2):
    global led_1_tab
    led_1_tab = [[0,0,0,0]]*nb_led_1;
    global led_2_tab
    led_2_tab = [[0,0,0,0]]*nb_led_2;
