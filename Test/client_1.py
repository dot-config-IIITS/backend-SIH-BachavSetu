from socketio import Client
from Routes.client_routes import client_routes
from Routes.admin_routes import admin_routes
from Routes.rescue_routes import rescue_routes


sio = Client()
sio.register_namespace(client_routes('/client'))
sio.register_namespace(rescue_routes('/rescue'))
sio.register_namespace(admin_routes('/admin'))

#temp variables 

from Routes.client_routes import temp

if __name__ == '__main__' :
    sio.connect('http://localhost:5000', namespaces=['/client'])
    print("connected")
    sio.emit('get_otp',{'phone':'9553323388'}, namespace='/client')
    print("exec 1")
    otp = input("Enter otp : ")
    sio.emit('verify_otp', {'phone':'9553323388','otp':otp}, namespace='/client')
    
    # sio.emit('verify_token',{'phone':temp.phone,'token':temp.token}, namespace='/client')
    sio.emit('add_details',temp.details,namespace='/client')
    sio.wait()

#LOnfoiherh