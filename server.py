import conf
import threading
from flask import Flask, request
from werkzeug.serving import make_server



class Server(threading.Thread):

    def __init__(self, event_inter):
        self.event_inter = event_inter
        threading.Thread.__init__(self)
        global app
        app = Flask(__name__)
        self.srv = make_server('127.0.0.1', 5000, app)

    def run(self):

        @app.route('/')
        def dire_coucou():
            conf.brightness += 10
            self.event_inter.set()
            return str(conf.brightness)

        print("Start Server")
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
