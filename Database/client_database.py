from pymongo import MongoClient

class SIDS_OTPS :
    def __init__(self) -> None:
        # self.phone_otp_pair = {'9553323388':'123456'}
        # self.sid_phone_pair = {}
        self.phone_otp_pair = {}
        self.sid_phone_pair = {}

# P-->phone S->SID, O->OTP, T->TOKEN
client_post = SIDS_OTPS()

class client_database :
    def __init__(self, mongo_uri) -> None:
        self.db = MongoClient(mongo_uri)['BachavSetu']['client']
    
    def verify_token(self, phone, token, sid) :
        user = self.db.find_one({'phone':phone})
        if (user) :
            if (token == user['token'] and token != '') :
                #Binding sid to phone no
                client_post.sid_phone_pair[sid] = phone

                if (user['name']!='') :
                    return {'status':'details_filled',
                            'name':user['name'], 'blood_group':user['blood_group'], 'emergency_contact':user['emergency_contact'],
                            'relation':user['relation'], 'dob':user['dob'], 'gender':user['gender']}
                else :
                    return {'status':'details_not_filled'}
            else :
                return {'status':'wrong_token'}
        else :
            return {'status':'user_doesn\'t_exist'}
        
    def add_details(self, phone, name, dob, blood_group, gender, emergency_contact, relation) :
        self.db.update_one({'phone':phone},{'$set':{'name':name, 'dob':dob, 'blood_group':blood_group,
                                                    'gender':gender, 'emergency_contact':emergency_contact,
                                                     'relation':relation }}) 
    def find_user(self, phone) :
        return self.db.find_one({'phone':phone})
    
    def update_token(self, phone, token) :
        self.db.update_one({'phone':phone},{"$set" : {"token":token}})

    def add_user(self, phone, token) :
        self.db.insert_one({'phone':phone, 'token':token , 
                            'name':'', 'dob':'', 'blood_group': '',
                            'emergency_contact':'','relation':''})
        
    # have to update this...
    def submit_feedback(self, phone, feedback, state, district) :
        if (state in states) :
            if (district in districts) :
                self.db.update_one({'phone':phone},{'$push':{'feedbacks':feedback}})
                feedback_id = feedback_db.insert_one({'state':state, 'district':district, 'feedback':feedback, 'phone':phone}).inserted_id
                admin_db.add_feedback(state = state, district = district, feedback_id = feedback_id)
                rescue_db.add_feedback(state = state, district = district, feedback_id = feedback_id)
            else :
                return {'status':'Invalid district'}
        else : 
            return {'status':'Invalid State'}

    # def user_exists(self, phone, type) :
    #     collection = None
    #     if (type == Type.ADMIN) :
    #         collection = self.admin_collection
    #     elif (type == Type.CLIENT) : 
    #         collection = self.client_collection
    #     elif (type == Type.RESCUE) :
    #         collection = self.rescue_colletion
    #     if (collection.find_one({'phone':phone})) :
    #         return 1
    #     else :
    #         return 0

    #LatLan(13.5553, 80.0267)