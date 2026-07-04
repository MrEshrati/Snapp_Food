class Order():
    def __init__(self,customer,items,time):
        self.customer = customer
        self.items = items
        self.time = time
        
    # def addItem(self):
    #     pass

    # def removeItem(self):
    #     pass
    
    def totalPrice(self):
        totalSum = 0
        for item in self.items[0]["items"]:
            totalSum += int(item["price"])
        return str(totalSum)