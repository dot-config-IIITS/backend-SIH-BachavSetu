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


local_ip = 'http://localhost:5000'
server_ip = 'https://bachavsetu.onrender.com'
url = local_ip
feedback = 'Hail .config'

def connect_to_server() :
    sio.connect(url,namespaces=['/client'])
    sio.reconnection = True
    sio.reconnection_attempts = float('inf')
    sio.reconnection_delay = 1
    print("Connected to "+url)

if __name__ == '__main__' :
    sio.connect(url,namespaces='/')
    sio.wait()

    connect_to_server()

    while (1) :
        option = int(input('Option : '))
        if (option == 0) :
            sio.disconnect()
            connect_to_server()
        elif (option == 1) :
            if (url ==  server_ip) :
                url = local_ip
            else :
                url = server_ip
        elif (option == 2) :
            sio.emit('get_otp',{'phone':'9553323388'}, namespace='/client')
            otp = input("Enter otp : ")
            sio.emit('verify_otp', {'phone':'9553323388','otp':otp}, namespace='/client')
        elif (option == 3) : 
            sio.emit('add_details',temp.details,namespace='/client')
        elif (option == 4) :
            token = input("Token : ")
            sio.emit('verify_token',{'phone':temp.phone,'token':token}, namespace='/client')
        elif (option == 5) :
            sio.emit()
        elif (option == 6) :
            sio.emit('logout')
        elif (option == 7) :
            sio.emit('submit_feedback', {'state' : 'Andhra Pradesh', 'district' : 'Anakapalli', 'feedback':feedback}, namespace='/client')
        elif (option == 8) :
            feedback = input("Enter new feedback")
        elif (option == -1) :
            quit(0)
    
    sio.wait()

            


