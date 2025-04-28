import connectModule as cM
from uuid import uuid4
import pymongo
 
 
#Adds customized items to cart. Features username to tie items to an account
#Takes in dictionary as input. Please notify if string/json is preferable.
'''
Example product input:
{
    '_id': ObjectId('679aafff3c458f74c616c9aa'),
    'itemName': 'Hotdog',
    'category': 'Not a sandwich',
    'price': 3.2,
    'freeItems': {
        'bun': True,
        'ketchup': False,
        'mustard': False
    },
    'freeToggleItems': [
        {'type': 'cheese', 'name': 'swiss', 'selected': false},
        {'type': 'cheese', 'name': 'provolone', 'selected': True}
    ],
    'paidItems': [
        {'name': 'Reaper Hot Sauce', 'price': 0.25, 'selected': False}
    ],
    'paidToggleItems': [
        {'type': 'Hotdog Upgrade', 'name': 'Beef Dog', 'price': 1.1, 'selected': False},
        {'type': 'Hotdog Upgrade', 'name': 'Chili Dog', 'price': 0.85, 'selected': False}
    ],
    'businessID': 'Protected'
}
'''
cartCollection = cM.mongoConnect("accountInfo", "shoppingCart")
orderCollection = cM.mongoConnect("accountInfo", "orderStatus")

# Adds customized items to the cart. Ties items to an account via the username.
def add_to_cart(product, username,quantity=None):
    # Creates a new unique ID for each product
    product.update({"username": username, "itemID": str(uuid4())})
    product.pop("_id",None)
    if quantity==None or quantity<1:
        quantity=1
    
    cartCollection.insert_one(product)
    # compute extras cost
    extras_cost = 0.0
    for extra in product.get("paidItems", []):
        if extra.get("selected", False):
            extras_cost += float(extra.get("price", 0.0))
    for toggle in product.get("paidToggleItems", []):
        if toggle.get("selected", False):
            extras_cost += float(toggle.get("price", 0.0))

    base_price = float(product.get("price", 0.0))
    product["totalPrice"] = (base_price + extras_cost) * quantity

    # insert into cart
    cartCollection.insert_one(product)
    return {"message": "Item successfully added to cart"}




# Marks items for checkout by giving them an orderID.
def checkout(username):
    orderID = str(uuid4())  # Generate a unique order ID for the entire order
    orderList = list(cartCollection.find({"username": username}))  # Retrieve all cart items for the user

    for order in orderList:
        order.update({"orderID": orderID, "orderStatus": "in_progress"})  # Update the order status and ID
        order.pop("_id", None)  # Remove _id to avoid duplicate key errors in MongoDB

    # Insert the cart items into the order collection
    result = orderCollection.insert_many(orderList)
    
    # Clear the user's cart after successful checkout
    cartCollection.delete_many({"username": username})
    
    return {"message": f"Checkout successful. Order #{orderID} has been created."}

# Retrieves all items in the cart for the specified username
def get_cart_items(username):
    cart_items = list(cartCollection.find({"username": username}))
    for item in cart_items:
        item.pop("_id", None)
    return cart_items

# Deletes a specific item from the user's cart based on itemID
def delete_item(username, itemID):
    result = cartCollection.delete_one({"username": username, "itemID": itemID})  # Delete the item
    
    if result.deleted_count > 0:
        return {"message": "Item successfully deleted from the cart."}
    else:
        return {"error": "Item not found or failed to delete."} 
import connectModule as cM

# Connect to the shopping cart collection
cartCollection = cM.mongoConnect("accountInfo", "shoppingCart")

def update_cart_item(username, itemID, updateFields):
    """
    Updates specific fields of a cart item for a given user.

    :param username: The username tied to the cart.
    :param itemID: The unique ID of the item in the cart.
    :param updateFields: A dictionary of fields to update (e.g., {'quantity': 2}).
    :return: A response dictionary with a success or error message.
    """

    # Ensure the updateFields dictionary is not empty
    if not updateFields:
        return {"error": "No valid fields provided for update."}

    # Ensure quantity is at least 1 if it's being updated
    if "quantity" in updateFields and updateFields["quantity"] < 1:
        return {"error": "Quantity must be at least 1."}

    # Perform the update in MongoDB
    result = cartCollection.update_one(
        {"username": username, "itemID": itemID},
        {"$set": updateFields}
    )

    # Check if the update was successful
    if result.matched_count == 0:
        return {"error": "Item not found or user mismatch."}
    elif result.modified_count == 0:
        return {"message": "No changes made."}
    else:
        return {"message": "Cart item updated successfully."}
