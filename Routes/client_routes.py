from flask_socketio import Namespace
from flask import request 
from ..Database.database import database

class client_routes(Namespace) :
    def on_connect(self):
        ssid = request.sid
        pass 

    def on_disconnect(self) :
        ssid = request.ssid
        pass 

    def on_login(self) : 
