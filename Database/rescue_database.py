from pymongo import MongoClient

class SIDS_OTPS:
    def __init__(self) -> None:
        self.phone_otp_pair = {}
        self.sid_phone_pair = {}

rescue_post = SIDS_OTPS()

class rescue_database :
    def __init__(self, mongo_uri) -> None:
        self.db = MongoClient(mongo_uri)['BachavSetu']['rescue']

    def verify_token(self, phone, token, sid) :
        user = self.db.find_one({'phone':phone})
        if (user) :
            if (token == user['token']) :
                #binding request.sid with phone no
                rescue_post.sid_phone_pair[sid] = phone
                
                return {'status':'success'}
            else :
                return {'status':'wrong_token'}
        else :
            return {'status':'user_doesn\'t_exist'}
        
    def find_user(self, phone) :
        return self.db.find_one({'phone':phone})
    
    def update_token(self, phone, token) :
        self.db.update_one({'phone':phone},{"$set" : {"token":token}})    