from socketio import ClientNamespace

class Temp :
    def __init__(self) -> None:
        self.phone = '9553323388'
        self.token = ''

        self.name = 'We don\'t care'
        self.blood_group = 'Sigala'
        self.gender = 'M'
        self.dob= '19'
        self.emergency_contact = '123'
        self.relation = 'Hmm'
        
        self.details = {'name':self.name , 'blood_group':self.blood_group , 'gender':self.gender, 
                        'emergency_contact':self.emergency_contact, 'relation':self.relation, 'dob':self.dob}
        
temp  = Temp()

class client_routes(ClientNamespace) :
    def on_verify_token_result(self, data):
        if ('token' in data) :
            temp.token = data['token']

    def on_verify_otp_result(self, data):
        print(data)

    def on_add_details_result(self, data): 
        print(data)