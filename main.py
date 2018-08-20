#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf
# Init all config variables
conf.init()

import controller
import threading
import server
import optparse

try:
    # Create events
    event_end_start = threading.Event()
    event_pause_run = threading.Event()

    # Create & Start flask server (thread)
    server = server.Server(event_end_start)
    server.start()

    # Create &  Start LED controller
    controller = controller.Controller(event_end_start)
    controller.run()


    server.join()
except KeyboardInterrupt:
    print("\nStopping program")
    controller.reset()
    server.shutdown()
