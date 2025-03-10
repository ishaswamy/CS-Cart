import connectModule as cM
import pymongo


menuCollection=cM.mongoConnect("Businesses","MenuItems")
menuCollection.create_index( { "itemName": 1, "businessID": 1},unique= True  )

'''
Add item features some optional parameters that can be left blank. If not in use, set the parameter to None, 0, or False.

The type section allows different toggleable items to be grouped into separate locations.

Here are some example inputs that feature multiple items:

freeItems = {
    "bun": True,
    "ketchup": False,
    "mustard": False
}

freeToggleItems = [
    {"type": "cheese", "name": "swiss", "selected": True},
    {"type": "cheese", "name": "provolone", "selected": True}
]

paidItems = [
    {"name": "Reaper Hot Sauce", "price": 0.25, "selected": False}.
    {"name": "Fake Reaper Cold Sauce", "price":0.25, "selected": False
]

paidToggleItems = [
    {"type": "Hotdog Upgrade", "name": "Beef Dog", "price": 1.1, "selected": False},
    {"type": "Hotdog Upgrade", "name": "Chili Dog", "price": 0.85, "selected": False}
]

'''
def addItem(itemName,category,price,businessID,freeItems=None, freeToggleItems=None, paidItems=None, paidToggleItems=None):
    menu_data={
            "itemName": itemName,

            "category": category,

            "price": float(price),

            "businessID":businessID,

            "freeItems": freeItems if freeItems else {},

            "freeToggleItems":freeToggleItems if freeToggleItems else {},

            "paidItems": paidItems if paidItems else {},

            "paidToggleItems": paidToggleItems if paidToggleItems else{}
    }

    try:

        menuCollection.insert_one(menu_data)

        return{"message": "added food"}
    except pymongo.errors.DuplicateKeyError:
        return{"message":"no food"}

def deleteItem(itemName,businessID):

    menuCollection.delete_one({"itemName":itemName,"businessID":businessID})
    return{"message":"Menu Item "+itemName+" successfully deleted."}


'''Update item function
Example of update_fields parameter:
update_data = {
    "price": 4.5,  # Update price
    "category": "Sandwich"  # Change category
}

'''
def updateItem(itemName, businessID, update_fields):
   result= menuCollection.update_one(
        {"itemName":itemName, "BusinessID":businessID}, #query
        {"$set":update_fields}#Update fields here
    ) 
   
   if result.matched_count==0:
        return {"message": "Item Not Found"}
   else:
        match result.modified_count:
            case 0:
                return {"message":"No changes made"}
            case _:
                return {"message": "Item succsessfully updated"}
    