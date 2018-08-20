import conf
import threading
import logging
from flask import Flask, request, redirect, render_template, jsonify
from werkzeug.serving import make_server


def set_debug():
    if conf.debug_serv == 0:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

def apply_change(self):
    if conf.start:
        conf.restart = True
        conf.start = False
        self.event_end_start.set()


class Server(threading.Thread):

    def __init__(self, event_end_start):
        set_debug()
        self.event_end_start = event_end_start
        threading.Thread.__init__(self)
        global app
        app = Flask(__name__)
        self.srv = make_server('127.0.0.1', 5000, app)

    def run(self):
        @app.route('/')
        def default_page():
            return render_template('index.html')

        @app.route('/start')
        def start():
            if not conf.start:
                conf.start = True
                self.event_end_start.set()
            return 'start ok',200

        @app.route('/restart')
        def restart():
            if conf.start:
                conf.restart = True
                conf.start = False
                self.event_end_start.set()
            return 'restart ok',200

        @app.route('/stop')
        def stop():
            if conf.start:
                conf.start = False
                self.event_end_start.set()
            return 'stop ok',200

        @app.route('/state')
        def state():
            state = "stopped"
            if conf.start:
                state = "started"
            return jsonify({'state': state, 'program': conf.current}),200

        @app.route('/setTheaterChaseRainbow')
        def setTheaterChaseRainbow():
            conf.current = "THEATER_CHASE_RAINBOW"
            apply_change(self)
            return 'setRainbow ok',200

        @app.route('/setRainbow')
        def setRainbow():
            conf.current = "RAINBOW"
            apply_change(self)
            return 'setRainbow ok',200

        @app.route('/setRainbowCycle')
        def setRainbowCycle():
            conf.current = "RAINBOW_CYCLE"
            apply_change(self)
            return 'setRainbowCycle ok',200

        @app.route('/setAll')
        def setAll():
            conf.current = "ALL"
            apply_change(self)
            return 'setAll ok',200

        @app.route('/setFixedColor', methods=['GET'])
        def setFixedColor():
            if request.args.get('r') != None:
                conf.color[0] = int(request.args.get('r'))
            if request.args.get('g') != None:
                conf.color[1] = int(request.args.get('g'))
            if request.args.get('b') != None:
                conf.color[2] = int(request.args.get('b'))
            conf.current = "FIXED_COLOR"
            apply_change(self)
            return 'setFixedColor ok',200


        print("#### Start Web Server ####")
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
