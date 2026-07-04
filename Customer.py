from db import DB
from Order import Order
from datetime import datetime
class Customer:
    def __init__(self,userId):
        self.db = DB()
        self.userId = userId
        self.cart = self.db.GetData("Cart",{"userId": self.userId})
        self.orders = []
    
    def addToCart(self,item):
            
        if len(self.cart) < 1:

            self.db.PostData("Cart",{
                "items":[item],
                "userId": self.userId,
            })
        else:
            oldLst = self.cart[0]["items"]
            oldLst.append(item)
            self.db.UpdateData("Cart",{"userId" : self.userId},{"$set" : {
                "items": oldLst
            }})
            
    def removeFromCart(self,item):
        oldLst = self.cart[0]["items"]
        for i in range(len(oldLst)):
            if oldLst[i] == item:
                del oldLst[i]      
                break 
        self.db.UpdateData("Cart",{"userId" : self.userId},{"$set" : {
            "items": oldLst
        }})
        
    def submitCart(self,customer):
        order_time = datetime.now().isoformat()
        order = Order(customer,self.cart,order_time)
        orderObj = {
            "customer": order.customer,
            "items": order.items,
            "time": order.time,
            "totalPrice": order.totalPrice(),
        }
        self.db.PostData("Orders",orderObj)
        self.emptyCart(self.cart[0]["_id"])
        return orderObj
    
    def emptyCart(self,cartId):
        self.db.DeleteData("Cart",{"_id":cartId})
    
    def showOrders(self,user):
        return self.db.GetData("Orders",{"customer": user})