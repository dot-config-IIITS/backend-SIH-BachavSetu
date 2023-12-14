from pymongo import MongoClient
from config import mongo_uri
from Database.rescue_database import rescue_database

class admin_database :

    db = MongoClient(mongo_uri)['BachavSetu']['admin']

    def add_feedback(feedback_id, state, district) :
        admin_database.db.update_one({'state':state, 'district':district}, {'$push':{'feedback_ids':feedback_id}})

    def add_admin(state, district, state_code) :
        admin_database.db.insert_one({'state':state, 'state_code' : state_code , 'district':district, 'feedback_ids':[]}) 

    def add_rescue(state, district, phone) :
        admin_database.db.update_one({'district':district, 'state':state}, {'$push':{'rescue_members' : phone}})
        rescue_database.add_rescue(state=state, district=district, phone=phone)

if (__name__ == "__main__") :
    from states_districts import states_districts
    for state_code in states_districts :
        state = states_districts[state_code]['name']
        districts = states_districts[state_code]['districts']
        for district in districts :
            admin_database.add_admin(state = state, district = district, state_code = state_code)
