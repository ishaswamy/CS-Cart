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