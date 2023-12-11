from flask import Flask
from flask_socketio import SocketIO
from config import mongo_uri

app = Flask(__name__)
socketio = SocketIO(app)


# client_ssids = {}
# admin_ssids = {}
# rescue_ssids = {}

from Routes.admin_routes import admin_routes
from Routes.client_routes import client_routes
from Routes.rescue_routes import rescue_routes

# Register the namespace with SocketIO
socketio.on_namespace(admin_routes('/admin'))
socketio.on_namespace(client_routes('/client'))
socketio.on_namespace(rescue_routes('/rescue'))

if __name__ == '__main__':
    # Run the Flask app with SocketIO
    socketio.run(app, debug=True)
