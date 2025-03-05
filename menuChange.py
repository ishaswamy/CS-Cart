import connectModule as cM
import pymongo
from pymongo import ASCENDING

menuCollection=cM.mongoConnect("Businesses","MenuItems")
menuCollection.create_index( { "itemName": 1, "businessID": 1},unique= True  )


def addItem(itemName,category,price,businessID):
    menu_data={
            "itemName": itemName,

            "category": category,

            "price": float(price),

            "businessID":businessID
    }

    try:

        menuCollection.insert_one(menu_data)

        return{"message": "added food"}
    except pymongo.errors.DuplicateKeyError:
        return{"message":"no food"}

def deleteItem(itemName,businessID):
    query_filter = { "borough": "Brooklyn" }


    menuCollection.delete_one({"itemName":itemName,"businessID":businessID})
    return{"message":"Menu Item "+itemName+" successfully deleted."}

def updateItem(itemName):
    return "lol"