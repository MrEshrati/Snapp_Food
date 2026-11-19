import pymongo

class DB:
    def __init__(self):  
        mongodb = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = mongodb["Snapp_Food"]
        self.users = self.db["Users"]
        self.restaurants = self.db["Restaurants"]
        self.items = self.db["Items"]
        self.cart = self.db["Cart"]
        self.order = self.db["Orders"]
        
    def PostData(self,collection_name,data):
        if collection_name == "Users":
            self.users.insert_one(data)
        elif collection_name == "Restaurants":
            self.restaurants.insert_one(data)
        elif collection_name == "Items":
            self.items.insert_one(data)
        elif collection_name == "Cart":
            self.cart.insert_one(data)
        elif collection_name == "Orders":
            self.order.insert_one(data)
    
    def upgrade_password(self, user_id, old_password, password_hash):
        result = self.users.update_one(
            {"_id": user_id, "password": old_password, "password_hash": {"$exists": False}},
            {"$set": {"password_hash": password_hash}, "$unset": {"password": ""}},
        )
        return result.modified_count == 1

    def GetData(self,collectoin_name,query):
        if collectoin_name == "Users":
            userList = []
            if query == "":
                for user in self.users.find():
                    userList.append(user)
            else:
                for user in self.users.find(query):
                    userList.append(user)
            return userList
        elif collectoin_name == "Restaurants":
            restaurantList = []
            if query == "":
                for restaurant in self.restaurants.find():
                    restaurantList.append(restaurant)
            else:
                for restaurant in self.restaurants.find(query):
                    restaurantList.append(restaurant)
            return restaurantList
        elif collectoin_name == "Items":
            itemList = []
            for item in self.items.find(query):
                itemList.append(item)
            return itemList
        elif collectoin_name == "Cart":
            cartList = []
            for c in self.cart.find(query):
                cartList.append(c)
            return cartList
        elif collectoin_name == "Orders":
            orderList = []
            for o in self.order.find(query):
                orderList.append(o)
            return orderList
        
    def DeleteData(self,collection_name,query):
        if collection_name == "Items":
            self.items.delete_one(query)
        elif collection_name == "Cart":
            self.cart.delete_one(query)
            
    def UpdateData(self,collection_name,query,newValues):
        if collection_name == "Items":
            self.items.update_many(query,newValues)
        elif collection_name == "Cart":
            self.cart.update_many(query,newValues)
        elif collection_name == "Restaurants":
            self.restaurants.update_many(query,newValues)

