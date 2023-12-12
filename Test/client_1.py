from socketio import Client
from Routes.client_routes import client_routes
from Routes.admin_routes import admin_routes
from Routes.rescue_routes import rescue_routes


sio = Client()
sio.register_namespace(client_routes('/client'))
sio.register_namespace(rescue_routes('/rescue'))
sio.register_namespace(admin_routes('/admin'))

#temp variables 
class Temp :
    def __init__(self) -> None:
        self.phone = '9553323388'
        self.token = 'hNWco7srQ1UltEErHqEs9RR1DWtBGRQCxnd1E7OVF8zPPjSTNhzYhS8Wme9K04K1RfmZOlLRvUVW4so5tqxV6RoFuepQgteLDkzEe5wHM5ruc0cC4NtAH8etd7rtIoY5'

        self.name = 'Hruthik'
        self.blood_group = 'O+'
        self.gender = 'M'
        self.age = '19'
        self.emergency_contact = '123'
        self.relation = 'Hmm'
        
        self.details = {'name':self.name , 'blood_group':self.blood_group , 'gender':self.gender, 
                        'emergency_contact':self.emergency_contact, 'relation':self.relation, 'age':self.age}

if __name__ == '__main__' :
    temp = Temp()
    sio.connect('http://localhost:5000', namespaces=['/client'])
    # sio.emit('get_otp',{'phone':'9553323388'}, namespace='/client')
    # sio.emit('verify_otp', {'phone':'9553323388','otp':'2662'}, namespace='/client')
    sio.emit('verify_token',{'phone':temp.phone,'token':temp.token}, namespace='/client')
    sio.emit('add_details',temp.details,namespace='/client')
    sio.wait()

#LOnfoiherh