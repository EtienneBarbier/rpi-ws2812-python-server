import conf
import threading
import logging
from flask import Flask, request, redirect, render_template, jsonify, Response
from werkzeug.serving import make_server
from flask_cors import CORS



def set_debug():
    if conf.debug_serv == 0:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

def apply_change(self):
    if conf.start:
        conf.restart = True
        conf.start = False
        self.event_end_start.set()

def start_led(self):
    if not conf.start:
        conf.start = True
        self.event_end_start.set()

def restart_led(self):
    if conf.start:
        conf.restart = True
        conf.start = False
        self.event_end_start.set()

def stop_led(self):
    if conf.start:
        conf.start = False
        self.event_end_start.set()


class Server(threading.Thread):

    def __init__(self, event_end_start):
        set_debug()
        self.event_end_start = event_end_start
        threading.Thread.__init__(self)
        global app
        app = Flask(__name__)
        CORS(app)
        self.srv = make_server('127.0.0.1', 5000, app)

    def run(self):
        @app.route('/')
        def default_page():
            return render_template('index.html')

        @app.route('/action', methods=['GET'])
        def action():
            if request.args.get('power') != None:
                arg_power = request.args.get('power')
                if arg_power == 'start':
                    start_led(self)
                elif arg_power == 'restart':
                    restart_led(self)
                elif arg_power == 'stop':
                    stop_led(self)
                else:
                    return Response(response=None,status=404,mimetype="application/json")
                return Response(response=None,status=200,mimetype="application/json")
            else:
                return Response(response=None,status=404,mimetype="application/json")


        @app.route('/state')
        def state():
            state = "stopped"
            if conf.start:
                state = "started"
            return Response(response={'state': state, 'program': conf.current},status=200,mimetype="application/json")


        @app.route('/annimation', methods=['GET'])
        def annimation():
            if request.args.get('id') != None:
                arg_annimation = request.args.get('id')
                if arg_annimation == 'theater_chase_rainbow':
                    conf.current = "THEATER_CHASE_RAINBOW"
                    apply_change(self)
                elif arg_annimation == 'rainbow':
                    conf.current = "RAINBOW"
                    apply_change(self)
                elif arg_annimation == 'rainbow_cycle':
                    conf.current = "RAINBOW_CYCLE"
                    apply_change(self)
                elif arg_annimation == 'all':
                    conf.current = "ALL"
                    apply_change(self)
                else:
                    return Response(response=None,status=404,mimetype="application/json")
                return Response(response=None,status=200,mimetype="application/json")
            else:
                return Response(response=None,status=404,mimetype="application/json")

        @app.route('/color', methods=['GET'])
        def setFixedColor():
            if request.args.get('red') != None:
                conf.color[0] = int(request.args.get('red'))
            if request.args.get('green') != None:
                conf.color[1] = int(request.args.get('green'))
            if request.args.get('blue') != None:
                conf.color[2] = int(request.args.get('blue'))
            conf.current = "FIXED_COLOR"
            apply_change(self)
            return Response(response=None,status=200,mimetype="application/json")


        print("#### Start Web Server ####")
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
