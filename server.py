import conf
import threading
from flask import Flask, request, redirect, render_template
from werkzeug.serving import make_server



class Server(threading.Thread):

    def __init__(self, event_end_start):
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
            return redirect("/")

        @app.route('/restart')
        def restart():
            if conf.start:
                conf.restart = True
                conf.start = False
                self.event_end_start.set()
            return redirect("/")

        @app.route('/setTheaterChaseRainbow')
        def setTheaterChaseRainbow():
            conf.current = "THEATER_CHASE_RAINBOW"
            return redirect("/")

        @app.route('/setRainbow')
        def setRainbow():
            conf.current = "RAINBOW"
            return redirect("/")

        @app.route('/setRainbowCycle')
        def setRainbowCycle():
            conf.current = "RAINBOW_CYCLE"
            return redirect("/")

        @app.route('/setAll')
        def setAll():
            conf.current = "ALL"
            return redirect("/")

        @app.route('/stop')
        def stop():
            if conf.start:
                conf.start = False
                self.event_end_start.set()
            return redirect("/")


        print("Start Server")
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
