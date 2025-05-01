import connectModule as cM
from flask import jsonify
from pymongo.errors import PyMongoError, OperationFailure

orderCollection=cM.mongoConnect("accountInfo","orderStatus")
historyCollection=cM.mongoConnect("Businesses","orderHistory")

''' 
note from isha 4/19/25, i believe these functions in this comment are unnecessary for the scope of our project but I left them in for now 
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


#Marks item with given ID as in progress
def markOrderInProgress(orderID):
    orderCollection.update_one({"orderID":orderID}, #query
        {"$set":{"orderStatus": "in_progress"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as in progress."}



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






'''
# Marks item with given itemID as completed
def markItemCompleted(itemID):
    orderCollection.update_one({"itemID": itemID}, 
        {"$set": {"itemStatus": "completed"}} 
    )
    return {f"message": f"Item {itemID} has been marked as completed."}

# Marks item with given itemID as in progress
def markItemInProgress(itemID):
    orderCollection.update_one({"itemID": itemID}, 
        {"$set": {"itemStatus": "in_progress"}} 
    )
    return {f"message": f"Item {itemID} has been marked as in progress."}


def clearOrder(orderID):
    
    try:
        docs = list(orderCollection.find({"orderID": orderID}))
        if docs:
            historyCollection.insert_many(docs)
            orderCollection.delete_many({"orderID": orderID})
            return {"message": f"Orders with Order ID {orderID} have been cleared from order queue"}
        else:
            return {"message": f"No orders found with Order ID {orderID}"}
    except (PyMongoError, OperationFailure) as e:
        return {"error": f"Failed to clear order: {str(e)}"}

def getOrderID(itemID):
    orderDict=orderCollection.find_one({"itemID":itemID},{"_id":0,"orderID":1})
    return orderDict["orderID"]

def getItemID(username):
    itemDict=list(orderCollection.find({"username":username},{"_id":0,"itemID":1}))
    return itemDict[0]["itemID"]
# Return all orders with their items and itemStatus 
def get_all_orders():
    orders = list(orderCollection.find({}, {"_id": 0, "itemID": 1, "itemStatus": 1, "itemName": 1, "category": 1, "totalPrice": 1, "orderID": 1}))
    return orders

#Return orders held by specific customer
def get_customer_orders(username): 
    orders = list(orderCollection.find({"username":username}, {"_id": 0, "itemID": 1, "itemStatus": 1, "itemName": 1, "category": 1, "totalPrice": 1, "orderID": 1}))
    return orders