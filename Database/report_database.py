from pymongo import MongoClient
from config import mongo_uri

class report_database :
    db = MongoClient(mongo_uri)['Cases']['report']

    def add_report(phone, coordinates, type, file_name, text) :
        return report_database.db.insert_one({'phone':phone , 'coordninates' : coordinates, 'type':type, 'file_name':file_name, 'text':text}).inserted_id
