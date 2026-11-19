# Uncomment these imports with the optional demo user blocks below.
# import os
# from passwords import hash_password

from Platform import Platform
from db import DB

db = DB()

# db.PostData("Users",{
#     "_id": "m1",
#     "name": "FirstManager",
#     "username": os.environ["SNAPP_DEMO_MANAGER_USERNAME"],
#     "password_hash": hash_password(os.environ["SNAPP_DEMO_MANAGER_PASSWORD"]),
# })

# db.PostData("Restaurants",{
#     "_id": "r1",
#     "name": "McDonalds",
#     "managerId": "m1",
#     "orders": [],
# })

# db.PostData("Items",{
#     "name": "Pizza",
#     "price": "150",
#     "isAvailable": "Available",
#     "itemType": "Food",
#     "restaurantId": "r1"
# })

# db.PostData("Items",{
#     "name": "Coca Cola",
#     "price": "20",
#     "isAvailable": "Available",
#     "itemType": "Drink",
#     "restaurantId": "r1"
# })

# db.PostData("Items",{
#     "name": "Burger",
#     "price": "100",
#     "isAvailable": "NotAvailable",
#     "itemType": "Food",
#     "restaurantId": "r1"
# })

# db.PostData("Users",{
#     "_id": "c1",
#     "name": "FirstCustomer",
#     "username": os.environ["SNAPP_DEMO_CUSTOMER_USERNAME"],
#     "password_hash": hash_password(os.environ["SNAPP_DEMO_CUSTOMER_PASSWORD"]),
# })

app = Platform()
app.Run()