from pymongo import MongoClient
from config import mongo_uri

class current_cases_database :
    db = MongoClient(mongo_uri)['Cases']['current_cases']
    
    def add_case(coordinate, type:str, radius:float, report_id) :
        return current_cases_database.db.insert_one({'coordinates':coordinate, 'type':type, 'radius':radius, 'reports':[report_id]}).inserted_id
    
    def update_radius(id, radius) :
        current_cases_database.db.update_one({'id':id}, {'radius':radius})
    # def complete_case(id) :
    #     document.find_element_
    #     pass 
    