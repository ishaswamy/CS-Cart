import connectModule as cM
from flask import jsonify

orderCollection=cM.mongoConnect("accountInfo","orderStatus")

#Marks order with given orderID as completed. Allows for updating of status entire order at once
def markOrderCompleted(orderID):
    orderCollection.update_many({"orderID":orderID}, #query
        {"$set":{"orderStatus": "completed"}}#Update fields here
    )
    return {f"message":"Order {orderID} has been marked as completed."}

#Marks order with given orderID as incomplete. Allows for updating of status entire order at once
def markOrderIncomplete(orderID):
    orderCollection.update_many({"orderID":orderID}, #query
        {"$set":{"orderStatus": "incomplete"}}#Update fields here
    )
    return {f"message":"Order {orderID} has been marked as incomplete."}

#Marks item with given ID as completed
def markItemCompleted(itemID):
    orderCollection.update_one({"itemID":itemID}, #query
        {"$set":{"orderStatus": "completed"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as completed."}

#Marks item with given ID as incomplete
def markItemIncomplete(itemID):
    orderCollection.update_one({"itemID":itemID}, #query
        {"$set":{"orderStatus": "incomplete"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as incomplete."}

#Marks item with given ID as in progress
def markOrderInProgress(orderID):
    orderCollection.update_one({"orderID":orderID}, #query
        {"$set":{"orderStatus": "in_progress"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as in progress."}

#Clears items in a given order from the order status collection.
def clearOrder(orderID):
    orderCollection.delete_many({"orderID":orderID})
    return {f"message":"Orders with Order ID {orderID} have been cleared from order queue"}

#Deletes specific items from the order status collection.
def clearItem(itemID):
    orderCollection.delete_one({"itemID":itemID})
    return {f"message":"Item with Item ID {itemID} has been cleared from order queue"}

def getOrderID(itemID):
    orderDict=orderCollection.find_one({"itemID":itemID},{"_id":0,"orderID":1})
    return orderDict["orderID"]

def getItemID(username):
    itemDict=list(orderCollection.find({"username":username},{"_id":0,"itemID":1}))
    return itemDict[0]["itemID"]

def get_all_orders():
    orders = list(orderCollection.find({}, {"_id": 0})) 
    return orders  # Return the list of orders
