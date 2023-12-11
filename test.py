import socketio

# Create a SocketIO client
sio = socketio.Client()

# Define an event handler for the 'my_response' event
@sio.event
def my_response(data):
    print('Server response:', data)

# Connect to the server
sio.connect('http://localhost:5000', namespaces=['/mynamespace'])

# Emit a custom event to the server
sio.emit('my_custom_event', {'data': 'Hello from Python client'}, namespace='/mynamespace')

# Wait for the server's response
sio.wait()

# Disconnect from the server
sio.disconnect()
