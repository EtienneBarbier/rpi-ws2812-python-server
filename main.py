#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf
import controller
import threading
import server


try:
    # Init all config variables
    conf.init()

    # Create events
    event_end_start = threading.Event()
    event_pause_run = threading.Event()

    # Create & Start flask server (thread)
    server = server.Server(event_inter)
    server.start()

    # Create &  Start LED controller
    controller = controller.Controller(event_inter)
    controller.run()


    server.join()
except KeyboardInterrupt:
    print("\nStopping program")
    controller.reset()
    server.shutdown()
