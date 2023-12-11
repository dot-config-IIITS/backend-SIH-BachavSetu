from pymongo import MongoClient

class client_database :
    def __init__(self, mongo_uri) -> None:
        self.db = MongoClient(mongo_uri)['BachavSetu']['client']
    
    def verify_token(self, phone_no, token) :
        user = self.db.find_one({'phone_no':phone_no})
        if (user) :
            if (token in user['tokens']) :
                if (user['name']!='') :
                    #make changes here...
                    return {'status':'details filled'}
                
                else :
                    return {'status':'details not filled'}
            else :
                return {'status':'token not present'}
        else :
            return {'status':'user doesn\'t exist'}

    # def user_exists(self, phone_no, type) :
    #     collection = None
    #     if (type == Type.ADMIN) :
    #         collection = self.admin_collection
    #     elif (type == Type.CLIENT) : 
    #         collection = self.client_collection
    #     elif (type == Type.RESCUE) :
    #         collection = self.rescue_colletion
    #     if (collection.find_one({'phone_no':phone_no})) :
    #         return 1
    #     else :
    #         return 0
        