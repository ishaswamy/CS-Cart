from dotenv import load_dotenv
import os
load_dotenv()  # This line brings all environment variables from .env into os.environ

#import customer account login/signup
'''import menuChange as mChan
import orderStatus as orStat
import shoppingCart as sCart
from bson import ObjectId'''
from app import getBusinessID
from bson.objectid import ObjectId
from customerAcc import get_accountType
#import shoppingCart
#import orderStatus

def n():
    print()

exampleProduct={
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
        {'type': 'cheese', 'name': 'swiss', 'selected': False},
        {'type': 'cheese', 'name': 'provolone', 'selected': True}
    ],
    'paidItems': [
        {'name': 'Reaper Hot Sauce', 'price': 0.25, 'selected': True}
    ],
    'paidToggleItems': [
        {'type': 'Hotdog Upgrade', 'name': 'Beef Dog', 'price': 1.1, 'selected': False},
        {'type': 'Hotdog Upgrade', 'name': 'Chili Dog', 'price': 0.85, 'selected': False}
    ],
    'businessID': 'Protected'
}

#print(getBusinessID())

'''
shoppingCart.add_to_cart(exampleProduct,"akumar")
shoppingCart.checkout("akumar")
#'''
'''
itemID=orderStatus.getItemID("akumar")
orderID=orderStatus.getOrderID(itemID)
#orderStatus.clearItem(itemID)
orderID=orderStatus.clearOrder(orderID)
#'''


from connectModule import mongoConnect
businessInfo=mongoConnect("Businesses","businessInfo")
    #Queries mongodb for the address and zipcode
address=businessInfo.find_one({"businessID":getBusinessID()},
                                  {"_id":0,"address":1,"zipCode":1})
addressSTR=(f"{address["address"]+", "+address["zipCode"]}")
print(addressSTR)

get_accountType("akumar")