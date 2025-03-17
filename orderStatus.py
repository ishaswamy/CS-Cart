import connectModule as cM

orderCollection=cM.mongoConnect("accountInfo","orderStatus")

#Marks item with given ID as completed
def markCompleted(itemID):
    orderCollection.update_one({"itemID":itemID}, #query
        {"$set":{"orderStatus": "completed"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as completed."}

#Marks item with given ID as incomplete
def markIncompleted(itemID):
    orderCollection.update_one({"itemID":itemID}, #query
        {"$set":{"orderStatus": "incomplete"}}#Update fields here
    )
    return {f"message":"Item {itemID} has been marked as incomplete."}

#Clears items in a given order from the order status collection.
def clearOrders(orderID):
    orderCollection.delete_many({"orderID":orderID})
    return {f"message":"Orders with Order ID {orderID} have been cleared"}

#Deletes specific items from the order status collection.

def clearItem(itemID):
    orderCollection.delete_one({"itemID":itemID})
    return {f"message":"Item with Item ID {itemID} has been cleared"}