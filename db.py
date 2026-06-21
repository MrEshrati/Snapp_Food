import pymongo

class DB:
    def __init__(self):  
        mongodb = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = mongodb["Snapp_Food"]
        self.users = self.db["Users"]
        
    def PostData(self,collection_name):
        pass
    
    def GetData(self,collectoin_name):
        pass

