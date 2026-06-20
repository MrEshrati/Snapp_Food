import pymongo

mongodb = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongodb["Snapp_Food"]

users = db["Users"]

