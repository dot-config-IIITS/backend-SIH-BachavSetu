from socketio import Client
from Routes.client_routes import client_routes
from Routes.admin_routes import admin_routes
from Routes.rescue_routes import rescue_routes


sio = Client()
sio.register_namespace(client_routes('/client'))
sio.register_namespace(rescue_routes('/rescue'))
sio.register_namespace(admin_routes('/admin'))

if __name__ == '__main__' :
    sio.connect('http://localhost:5000', namespaces=['/client'])
    sio.emit('get_otp',{'phone':'8520052225'}, namespace='/client')
    # sio.emit('verify_token', {'phone': '123', 'token':'1234'}, namespace='/client')
    sio.wait()

#LOnfoiherh