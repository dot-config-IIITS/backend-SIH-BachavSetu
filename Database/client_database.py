from pymongo import MongoClient

class SIDS_OTPS :
    def __init__(self) -> None:
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
            if (token in user['tokens']) :
                client_post.sid_phone_pair[sid] = phone
                if (user['name']!='') :
                    #make changes here...
                    return {'status':'details filled'}
                
                else :
                    return {'status':'details not filled'}
            else :
                return {'status':'token not present'}
        else :
            return {'status':'user doesn\'t exist'}
        
    def add_details(self, phone, name, age, blood_group, gender, emergency_contact, relation) :
        if (self.db.update_one({'phone':phone},{'$set':{'name':name, 'age':age, 'blood_group':blood_group,
                                                    'gender':gender, 'emergency_contact':emergency_contact,
                                                     'relation':relation }}) ) > 0 :
            return {'status':'success'}
        else :
            return {'status':'user not found'}

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