import connectModule as cM
import pymongo

#Connecting to mongoDB collection
menuCollection=cM.mongoConnect("Businesses","menuItems")
userLoginCollection=cM.mongoConnect("accountInfo","userInformation")
categoryCollection=cM.mongoConnect("Businesses","menuCategories")

#Creating filter to prevent businesses from creating duplicates of the same item
menuCollection.create_index( { "itemName": 1, "businessID": 1},unique= True  )
categoryCollection.create_index({ "category": 1, "businessID": 1},unique= True  )

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

def addItem(update_fields):
    menu_data=update_fields
    try:
        menuCollection.insert_one(menu_data)
    except pymongo.errors.DuplicateKeyError:
        return{"message":"Item already exists in the menu."}

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


def updateItem(item_id, update_fields):
   result= menuCollection.update_one(
        {"itemID":item_id}, #query
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
def get_menu_items(businessID):
    
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

def get_item(item_id):
    item = menuCollection.find_one({"itemID": (item_id)})
    return item

def get_categories(businessID):
    if not businessID:
        return []

    category_collection = cM.mongoConnect("Businesses", "menuCategories")
    categories = list(category_collection.find({"businessID": str(businessID)}))

    for category in categories:
        category.pop("_id", None)

    return categories
def addCategory(categoryName,businessID,categoryImageURL):
    category_data={
        "category":categoryName,
        "businessID":businessID,
        "categoryImageURL":categoryImageURL
    }
    try:

        categoryCollection.insert_one(category_data)

        return{"message": "added "+categoryName+" to the category."}
    except pymongo.errors.DuplicateKeyError:
        return{"message":"Item "+categoryName+" already exists in the menu."}
