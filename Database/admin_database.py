from pymongo import MongoClient
from config import mongo_uri
from Database.rescue_database import rescue_database
from Functions.functions import hash_sha512, gen_token

team_types = ['police', 'medical', 'fire', 'ndrf', 'coast_guard', 'ngo' ]

class admin_cache :
    # sid : {state district}
    ssd_pair = {}

class admin_database :

    db = MongoClient(mongo_uri)['admin_database']

    def login(state, district, password, sid) :
        if (state in admin_database.db.list_collection_names()):
            admin = admin_database.db[state].find_one({'district' : district})
            if (admin) :
                hash_val = hash_sha512(password)
                if (admin['hash_val'] == hash_val) :        
                                
                    admin_cache.ssd_pair[sid] = {'state':state, 'district':district}

                    token = gen_token()
                    admin_database.db[state].update_one({'district':district},{'token':token})

                    #gotta update reagarding what to update
                    return {'status' : 'success', 'token' : token}
                else :
                    return {'status' : 'wrong_password'}
            else :
                return {'status' : 'Invalid district'}
        else :
            return {'status' : 'Invalid state'}

    def verify_token(district, state, token):
        if (state in admin_database.db.list_collection_names()):
            admin = admin_database.db[state].find_one({'district' : district})
            if (admin) :
                if (admin['token'] == token) :
                    # gotta update, regarding what to return
                    return {'status' : 'success'}
                else :
                    return {'status' : 'wrong_token'}
            else :
                return {'status' : 'Invalid district'}
        else :
            return {'status' : 'Invalid state'}        

    def add_feedback(feedback_id, state, district) :
        admin_database.db[state].update_one({'district':district}, {'$push':{'feedback_ids':feedback_id}})

    # route cannot be accessed by admins for security reasons, admins have to contact the database owners
    def add_admin(state, district) :
        admin_database.db.create_collection(state)
        admin_database.db[state].create_index([("district",1)],unique=True)
        members = {}
        for type in team_types :
            members[type] = []
        admin_database.db[state].insert_one({'district':district, 'feedback_ids':[], 'token':"", 
                                             'members':members })

    def add_rescue_team(state, district, phone, type) :
        if (type in team_types) :
            result = admin_database.db[state].update_one({'district':district},{'$addToSet':{f'members.{type}':phone}})
            if (result.modified_count == 1) :
                return {'status':'success'}
            else :
                return {'status':'Member '+phone+' already exists in '+type}
        else :
            return {'status':'Invalid team type'}


if (__name__ == "__main__") :
    from states_districts import states_districts
    for state_code in states_districts :
        state = states_districts[state_code]['name']
        districts = states_districts[state_code]['districts']
        for district in districts :
            admin_database.add_admin(state = state, district = district, state_code = state_code)
