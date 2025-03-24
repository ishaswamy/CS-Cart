from dotenv import load_dotenv
import os
load_dotenv()  # This line brings all environment variables from .env into os.environ

#import customer account login/signup
import customerAcc as cAcc
import menuChange as mChan
import orderStatus as orStat
import shoppingCart as sCart
from bson import ObjectId

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

'''
print("Adding exampleProducts to cart:")
print(sCart.add_to_cart(exampleProduct,"zivywivy"))
print(sCart.add_to_cart(exampleProduct,"zivywivy"))
print(sCart.add_to_cart(exampleProduct,"zivywivy",3))
#'''

'''
print("Checking out exampleProduct:")
print(sCart.checkout("zivywivy"))

#'''



'''
exampleOrdID=orStat.getOrderID(orStat.getItemID("zivywivy"))
print("Changing order status of exampleProduct to complete:")
print(orStat.markOrderCompleted(exampleOrdID))
#'''

'''
exampleOrdID=orStat.getOrderID(orStat.getItemID("zivywivy"))
print("Changing order status of exampleProduct to incomplete:")
print(orStat.markOrderIncomplete(exampleOrdID))
#'''

'''
exampleOrdID=orStat.getOrderID(orStat.getItemID("zivywivy"))
print("Clearing order from orderStatus collection:")
print(orStat.clearOrder(exampleOrdID))
#'''

'''
print("Adding exampleProduct to cart:"+sCart.add_to_cart(exampleProduct,"zivywivy"))
print("Checking out exampleProduct:"+sCart.checkout("zivywivy"))

exampleItemID=orStat.getItemID("zivywivy")
print("Changing individual item status of exampleProduct to complete:"+orStat.markItemCompleted(exampleItemID))
print("Changing individual item status of exampleProduct to incomplete:"+orStat.markItemIncomplete(exampleOrdID))

#'''

'''
#print("Clearing individual item from orderStatus collection:")
#print(orStat.clearItem(exampleItemID))
#'''

'''
print("\nRegular registration of new user")
print(cAcc.register_user("testUsername","testEmail@test.com","testPass123",1))
print("\ntesting if duplicate username AND email allowed")
print(cAcc.register_user("testUsername","testEmail@test.com","testPass123",1))
print("\ntesting if duplicate email allowed")
print(cAcc.register_user("testUsername2","testEmail@test.com","testPass123",1))
print("\ntesting if duplicate username allowed")
print(cAcc.register_user("testUsername","testEmail2@test.com","testPass123",1))


# Test Cases
print("\nSuccessful login test")
print(cAcc.login_user("testUsername", "testPass123"))  # Should return success
print("\nTesting invalid password")
print(cAcc.login_user("testUsername", "wrongPass")) #Returns incorrect user or password
print("\nTesting invalid username")
print(cAcc.login_user("wrongUser", "testPass123")) #Returns incorrect user or password

#

print(mChan.addItem("Dotdog","Hotdog",3.50,1))
print(mChan.addItem("Dotdog","Hotdog",3,2))
print(mChan.addItem("Dotdog","Hotdog",3.50,1))

print(mChan.deleteItem("Dotdog",2))

#print(mChan.deleteItem("Dotdog",1))
#print(mChan.deleteItem("Dotdog",2))

# Example 1: Add an item to the collection

result = mChan.addItem( 
    itemName="Hotdog", 
    category="Not a sandwich", 
    price=3.2, 
    businessID=1,
    freeItems={"bun": True, "ketchup": False, "mustard": False},
    freeToggleItems=[{"type": "cheese", "name": "Swiss", "selected": True}],
    paidItems=[{"name": "Reaper Hot Sauce", "price": 0.25, "selected": False}],
    paidToggleItems=[{"type": "Hotdog Upgrade", "name": "Beef Dog", "price": 1.1, "selected": False}]
)
print(result)

# Example 2: Update an existing item
result = mChan.updateItem(
    itemName="Hotdog", 
    businessID=1, 
    update_fields={"price": 4.5, "category": "Sandwich"}
)
print(result)

# Example 3: Trying to update an item that doesn't exist
result = mChan.updateItem(
    itemName="NonExistentItem",
    businessID=999,
    update_fields={"price": 5.0}
)
print(result)

# Example 4: Update an item without any changes (same price)
result = mChan.updateItem(
    itemName="Hotdog", 
    businessID=1,
    update_fields={"price": 4.5}  # No actual change
)

print(result)
'''