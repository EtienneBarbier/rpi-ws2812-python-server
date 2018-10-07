#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf
# Init all config variables
conf.init()

import controller
import threading
import server
import optparse

import shared
shared.init()


try:
    # Create events
    event_end_start = threading.Event()
    event_pause_run = threading.Event()

    # Create & Start flask server (thread)
    shared.server = server.Server(event_end_start)
    shared.server.start()

    # Create &  Start LED controller
    shared.controller = controller.Controller(event_end_start)
    shared.controller.run()


    shared.server.join()
except KeyboardInterrupt:
    print("\nStopping program")
    shared.controller.reset()
    shared.server.shutdown()
