# library imports
from pymongo import MongoClient

# user-defined classes imports
from Database.feedback_database import feedback_database
from Database.admin_database import admin_database

# variables imports
from config import mongo_uri
from Database.states_districts import state_district_pair_exists


# POS ->  P : phone, O : OTP,  S : SID 
class client_pos :
    phone_otp_pair = {}
    sid_phone_pair = {}

class client_database :
    db = MongoClient(mongo_uri)['BachavSetu']['client']
    
    def verify_token(phone, token, sid) :
        user = client_database.db.find_one({'phone':phone})
        if (user) :
            if (token == user['token'] and token != '') :
                # Binding sid to phone no
                client_pos.sid_phone_pair[sid] = phone

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
        
    def add_details(phone, name, dob, blood_group, gender, emergency_contact, relation) :
        client_database.db.update_one({'phone':phone},{'$set':{'name':name, 'dob':dob, 'blood_group':blood_group,
                                                    'gender':gender, 'emergency_contact':emergency_contact,
                                                     'relation':relation }}) 
    def find_client(phone) :
        return client_database.db.find_one({'phone':phone})
    
    def update_token(phone, token) :
        client_database.db.update_one({'phone':phone},{"$set" : {"token":token}})

    def add_client(phone, token) :
        client_database.db.insert_one({'phone':phone, 'token':token , 
                            'name':'', 'dob':'', 'blood_group': '', 
                            'emergency_contact':'','relation':'', 'feedback_ids' : [], 'report_ids':[]})
        
    # have to update this...
    def submit_feedback(phone, feedback, state, district) :
        if state_district_pair_exists(state=state, district=district) :
            feedback_id = feedback_database.add_feedback(phone=phone, district=district, state=state, feedback=feedback)
            client_database.db.update_one({'phone':phone},{'$push':{'feedback_ids':feedback_id}})
            admin_database.add_feedback(state = state, district = district, feedback_id = feedback_id)
            return {'status':'Success'}
        else : 
            return {'status':'Invalid State or District or both'}