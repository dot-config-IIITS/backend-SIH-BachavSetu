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
            if (token == user['token']) :
                client_post.sid_phone_pair[sid] = phone
                if (user['name']!='') :
                    #make changes here...
                    return {'status':'details_filled'}
                
                else :
                    return {'status':'details_not_filled'}
            else :
                return {'status':'wrong_token'}
        else :
            return {'status':'user_doesn\'t_exist'}
        
    def add_details(self, phone, name, age, blood_group, gender, emergency_contact, relation) :
        self.db.update_one({'phone':phone},{'$set':{'name':name, 'age':age, 'blood_group':blood_group,
                                                    'gender':gender, 'emergency_contact':emergency_contact,
                                                     'relation':relation }}) 
    def find_user(self, phone) :
        return self.db.find_one({'phone':phone})
    
    def update_token(self, phone, token) :
        self.db.update_one({'phone':phone},{"$set" : {"token":token}})

    def add_user(self, phone, token) :
        self.db.insert_one({'phone':phone, 'token':token , 
                            'name':'', 'age':'', 'blood_group': '',
                            'emergency_contact':'','relation':''})

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