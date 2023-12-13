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

@app.route("/")
def hello_world():
    print("it works")
    return "Hi guys"

if __name__ == '__main__':
    # For server deployment
    socketio.run(app,  host='0.0.0.0', port=80, debug=True, allow_unsafe_werkzeug=True)

    # For local deployment
    # socketio.run(app,  host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
