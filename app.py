from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from Routes.admin_routes import admin_routes
from Routes.client_routes import client_routes
from Routes.rescue_routes import rescue_routes

socketio.on_namespace(admin_routes('/admin'))
socketio.on_namespace(client_routes('/client'))
socketio.on_namespace(rescue_routes('/rescue'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
