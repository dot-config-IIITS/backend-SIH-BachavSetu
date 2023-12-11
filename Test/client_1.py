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
        self.token = 'MDVeO7BjL0StpUOJKHUt4tsHnhjWEWFgyChjb9FVBe99PHo771vSgn85a7y5lA9VGXKdQOyLJmsbu6abG2IaHUTtpImseV8HhRqlgQhiNSVxC0PHzarpg096qhV0PvqE'
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
    # sio.emit('verify_otp', {'phone':'9553323388','otp':'123456'}, namespace='/client')
    sio.emit('verify_token',{'phone':temp.phone,'token':temp.token}, namespace='/client')
    sio.emit('add_details',temp.details,namespace='/client')
    sio.wait()

#LOnfoiherh