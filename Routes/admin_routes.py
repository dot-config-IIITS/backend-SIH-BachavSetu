from flask_socketio import Namespace
from flask import request 
# from ..app import admin_db

class admin_routes(Namespace) :
    def on_connect(self):
        sid = request.sid
        pass 

    def on_disconnect(self) :
        sid = request.ssid
        pass 