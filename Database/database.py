from pymongo import MongoClient

class Database :
    def __init__(self, mongo_uri) -> None:
        self.db = MongoClient(mongo_uri)['BachavSetu']
        self.client_collection = self.db['client']
        self.admin_collection = self.db['admin']
        self.rescue_colletion = self.db['rescue']