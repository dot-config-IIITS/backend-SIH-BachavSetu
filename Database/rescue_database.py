from pymongo import MongoClient
from config import mongo_uri

class rescue_cache:
    phone_otp_pair = {}

    # sid : {phone coordinates}
    spc_pair = {}

    # state_district rooms, need this to get the list of all
    # rescue members online at the moment..  
    sd_rooms = []
    # sid : {phone :  , district : , state : }
    # state_district : sid


class rescue_database :
    db = MongoClient(mongo_uri)['rescue_database']

    def verify_token(phone, token, state, district) :
        member = rescue_database.find_rescue(state=state, district=district, phone=phone)
        if (member['status'] == 'success') :
            if (member['token'] == token) :
                return {'status':'success'}
            else :
                return {'status':'Wrong token'}
        else :
            return member


        user = self.db.find_one({'phone':phone})
        if (user) :
            if (token == user['token']) :
                #binding request.sid with phone no
                rescue_cache.sid_phone_pair[sid] = phone
                
                return {'status':'success'}
            else :
                return {'status':'wrong_token'}
        else :
            return {'status':'user_doesn\'t_exist'}
        
    def find_rescue(phone, state, district) :
        if (state+"_"+district in rescue_database.db.list_collection_names()) :
            member = rescue_database.db[state+"_"+district].find_one({'phone':phone})
            if (member) :
                return {'status':'success', 'member':member}
            else :
                return {'status':'No rescue registered with the specific district and state'}
        else :
            return {'status':'Invalid state or state'}
        
        # return rescue_database.db['rescue_database'][state]
        # return rescue_database.db.find_one({'phone':phone})

    # def add_feedback(feedback_id, state, district) :
    #     rescue_database.db.update_one({'state':state, 'district':district}, {'$push':{'feedback_ids':feedback_id}})

    #To be used only from admin_database
    def add_rescue(state, district, phone) :
        rescue_database.db.insert_one({'state':state, 'district':district, 'phone':phone}) 

    def update_token(phone, token) :
        rescue_database.db.update_one({'phone':phone},{"$set" : {"token":token}})    

    def get_nearest_rescue_phones(state, district, coordinates:list) :
        pipeline = [
            {"$match": {'state':state, 'district':district}},
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": coordinates},
                    "distanceField": "distance",
                    "spherical": True,
                    "limit": 1
                }
            }
        ]
        rescue_centre = list(rescue_database.db.aggregate(pipeline = pipeline))[0]
        phones = rescue_centre['phones']
        return phones


