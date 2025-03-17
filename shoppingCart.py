import connectModule as cM
from uuid import uuid4
import pymongo

cartCollection=cM.mongoConnect("accountInfo","shoppingCart")
orderCollection=cM.mongoConnect("accountInfo","orderStatus")

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
        {'type': 'cheese', 'name': 'swiss', 'selected': True},
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
def add_to_cart(product,username):
    #Creates new unique ID
    product.update({"username":username,"itemID":uuid4()})
    
    cartCollection.insert_one(product)

    return {"message": "Item successfully added to cart"}

#Marks items for checkout by giving them an orderID that allows for the order to be marked as complete/incomplete
def checkout(username):
    #Generates unique ID for all items in the order
    orderID=uuid4()
    orderList=list(cartCollection.find({"username":username}))
    for order in orderList:
        order.update({"orderID":orderID,"orderStatus":"incomplete"})
        order.pop("_id", None)  # Remove _id to avoid duplicate key errors

    result = orderCollection.insert_many(orderList)
    cartCollection.delete_many({"username":username})

    return {f"message": "Checkout successful. Order #{orderID} has been created."}
