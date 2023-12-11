from flask_socketio import Namespace
from flask import request 

class rescue_routes(Namespace) :
    def on_connect(self):
        ssid = request.sid
        pass 

    def on_disconnect(self) :
        ssid = request.ssid
        pass 