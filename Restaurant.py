from db import DB
class Restaurant:
    def __init__(self,name,manager):
        self.db = DB()
        self.name = name,
        self.managerId = manager,
        self.menu = [],
        self.orders = [],
        
    def Menu(self,restaurantId):
        self.menu = self.db.GetData("Items",{"restaurantId":restaurantId})
        
    def Orders(self,resId):
        data = self.db.GetData("Restaurants",{"_id": resId});
        return data[0]["orders"]
    
    def newOrder(self,data,resId):
        resOrders = []
        newTotalPrice = 0
        for item in data["items"][0]["items"]:
            if item["restaurantId"] == resId:
                resOrders.append(item)
                newTotalPrice += int(item["price"])
                
        data["items"][0]["items"] = resOrders
        data["totalPrice"] = newTotalPrice
        oldOrders = (self.db.GetData("Restaurants",{"_id":resId}))[0]["orders"]
        oldOrders.append(data)
        self.db.UpdateData("Restaurants",{"_id": resId},{"$set": {
            "orders":oldOrders
        }})