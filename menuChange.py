import connectModule as cM
import pymongo

#Connecting to mongoDB collection
menuCollection=cM.mongoConnect("Businesses","menuItems")

userLoginCollection=cM.mongoConnect("accountInfo","userInformation")


#Creating filter to prevent businesses from creating duplicates of the same item
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
def addItem(itemName,category,price,businessID,freeItems=None, freeToggleItems=None,
             paidItems=None, paidToggleItems=None):
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

        return{"message": "added "+itemName+" to the menu."}
    except pymongo.errors.DuplicateKeyError:
        return{"message":"Item "+itemName+" already exists in the menu."}

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
        {"itemName":itemName, "businessID":businessID}, #query
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
    
# Retrieves all items in the cart for the specified username
def get_menu_items(username):
    
    businessID = int((userLoginCollection.find_one({"username": username}, {"businessID": 1})).get("businessID"))
    menu_items = list(menuCollection.find({"businessID": businessID}))  # Fetch menu items from MongoDB
    
    # Remove the "_id" field from each item to make the response cleaner
    for item in menu_items:
        item.pop("_id", None)

    return menu_items

def get_specific_category_items(businessID, category):
    if not businessID:  
       return []  # Return an empty list if businessID is missing
    
    menu_items = list(menuCollection.find({"businessID": businessID, "category": category}))
    
    for item in menu_items:
        item.pop("_id", None)
    
    return menu_items