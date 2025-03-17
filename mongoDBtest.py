from dotenv import load_dotenv
import os
load_dotenv()  # This line brings all environment variables from .env into os.environ

#import customer account login/signup
import customerAcc as cAcc
import menuChange as mChan

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

'''

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
'''
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