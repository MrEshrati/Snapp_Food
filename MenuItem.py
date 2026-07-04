class MenuItem:
    def __init__(self,name,price,state,itemType,restaurantId):
        self.name = name
        self.price = price
        self.isAvailable = state
        self.itemType = itemType
        self.restaurantId = restaurantId
        
    def itemInfo(self):
        return {
            "name": self.name,
            "price": self.price,
            "isAvailable": self.isAvailable,
            "itemType": self.itemType,
            "restaurantId": self.restaurantId
        }