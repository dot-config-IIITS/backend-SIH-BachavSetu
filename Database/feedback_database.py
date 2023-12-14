from pymongo import MongoClient
from config import mongo_uri

class feedback_database :
    db = MongoClient(mongo_uri)['BachavSetu']['feedback']
    
    def add_feedback(phone, state, district, feedback) :
        return feedback_database.db.insert_one({'state':state, 'district':district, 'feedback':feedback, 'phone':phone}).inserted_id