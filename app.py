from flask import Flask, request
from flask_socketio import SocketIO, rooms
from asyncio import ensure_future

from Routes.admin_routes import update_coordinates 

app = Flask(__name__)
socketio = SocketIO(app)

# from Routes.admin_routes import admin_routes
from Routes.client_routes import client_routes
# from Routes.rescue_routes import rescue_routes

# socketio.on_namespace(admin_routes('/admin'))
socketio.on_namespace(client_routes('/client'))
# socketio.on_namespace(rescue_routes('/rescue'))

@app.route("/")
def notify_server_status():
    return "Server is up"

@socketio.on('connect')
def update_coordinates_wrapper():
    ensure_future(update_coordinates(socketio))

if __name__ == '__main__':
    socketio.run(app,  host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)