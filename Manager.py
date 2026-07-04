from MenuItem import MenuItem
from db import DB
class Manager:
    def __init__(self,restaurantId):
        self.restaurantId = restaurantId
        self.db = DB()
        
    def addItem(self,name,price,status,itemType):
        item = MenuItem(name,price,status,itemType,self.restaurantId)
        self.db.PostData("Items",item.itemInfo())
    def editItem(self,name,price,status,itemType,itemId):
        item = MenuItem(name,price,status,itemType,self.restaurantId)
        self.db.UpdateData("Items",{"_id": itemId},{"$set" : item.itemInfo()})
    def deleteItem(self,itemId):
        self.db.DeleteData("Items",{"_id":itemId})