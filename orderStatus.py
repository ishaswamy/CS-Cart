import connectModule as cM
from flask import jsonify
from pymongo.errors import PyMongoError, OperationFailure
orderCollection=cM.mongoConnect("accountInfo","orderStatus")
historyCollection=cM.mongoConnect("Businesses","orderHistory")

#Marks order with given orderID as completed. Allows for updating of status entire order at once
def markOrderCompleted(orderID):
    orderCollection.update_many({"orderID":orderID}, #query
        {"$set":{"orderStatus": "completed"}}#Update fields here
    )
    return {f"message":"Order {orderID} has been marked as completed."}

#Marks order with given orderID as incomplete. Allows for updating of status entire order at once
def markOrderIncomplete(orderID):
    orderCollection.update_many({"orderID":orderID}, #query
        {"$set":{"orderStatus": "in progress"}}#Update fields here
    )
    return {f"message":"Order {orderID} has been marked as in progress."}

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
    return {f"message":"Item {itemID} has been marked as in progress."}

#Marks item with given ID as in progress
def markOrderInProgress(orderID):
    orderCollection.update_one({"orderID":orderID}, #query
        {"$set":{"orderStatus": "in_progress"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as in progress."}

#Clears items in a given order from the order status collection. Adds items in the given order to orderHistory collection.
def clearOrder(orderID):
    try:
        historyCollection.insert_many(orderCollection.find({"orderID":orderID}))
        orderCollection.delete_many({"orderID":orderID})
    except (PyMongoError, OperationFailure) as e:
        return {f"message":"Orders with Order ID {orderID} have been cleared from order queue"}

#Deletes specific items from the order status collection. Adds item to orderHistory collection.
def clearItem(itemID):
    try:
        item=orderCollection.find_one({"itemID":itemID})
        item.pop("_id")
        #Adds item to order history collection for archival purposes
        historyCollection.insert_one(item)

        #Deletes item from order status page
        orderCollection.delete_one({"itemID":itemID})
        return {f"message":"Item with Item ID {itemID} has been cleared from order queue"}
    except (PyMongoError, OperationFailure) as e:
        return(f"Insertion error: {e}")


def getOrderID(itemID):
    orderDict=orderCollection.find_one({"itemID":itemID},{"_id":0,"orderID":1})
    return orderDict["orderID"]

def getItemID(username):
    itemDict=list(orderCollection.find({"username":username},{"_id":0,"itemID":1}))
    return itemDict[0]["itemID"]

def get_all_orders():
    orders = list(orderCollection.find({}, {"_id": 0})) 
    return orders  # Return the list of orders
