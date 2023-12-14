from pymongo import MongoClient
from config import mongo_uri

class rescue_pos:
    phone_otp_pair = {}
    sid_phone_pair = {}


class rescue_database :
    db = MongoClient(mongo_uri)['BachavSetu']['rescue']

    def verify_token(self, phone, token, sid) :
        user = self.db.find_one({'phone':phone})
        if (user) :
            if (token == user['token']) :
                #binding request.sid with phone no
                rescue_pos.sid_phone_pair[sid] = phone
                
                return {'status':'success'}
            else :
                return {'status':'wrong_token'}
        else :
            return {'status':'user_doesn\'t_exist'}
        
    def find_rescue(phone) :
        return rescue_database.db.find_one({'phone':phone})

    # def add_feedback(feedback_id, state, district) :
    #     rescue_database.db.update_one({'state':state, 'district':district}, {'$push':{'feedback_ids':feedback_id}})

    #To be used only from admin_database
    def add_rescue(state, district, phone) :
        rescue_database.db.insert_one({'state':state, 'district':district, 'phone':phone}) 

    def update_token(phone, token) :
        rescue_database.db.update_one({'phone':phone},{"$set" : {"token":token}})    